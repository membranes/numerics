"""Module interface.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.analytics.architecture
import src.analytics.bullet
import src.analytics.cost
import src.analytics.derivations
import src.analytics.limits
import src.analytics.spider
import src.elements.limits as lm
import src.elements.s3_parameters as s3p
import src.functions.directories
import src.functions.objects


class Interface:
    """
    Class Interface
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()
        self.__storage()

        # The architecture name of the best model, ...
        self.__architecture: str = src.analytics.architecture.Architecture().exc()

    def __storage(self):
        """
        Creates all the paths for the graphing & serving data.

        :return:
        """

        directories = src.functions.directories.Directories()

        for value in self.__configurations.graphs_:
            directories.create(value)

    def __cases(self) -> pd.DataFrame:
        """

        :return: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                 The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        """

        path = os.path.join(
            self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)
        cases = src.functions.objects.Objects().frame(path=path, orient='index')

        return cases

    @staticmethod
    def __derivations(cases: pd.DataFrame) -> pd.DataFrame:
        """
        Appends a series of metrics to each instance.

        :param cases: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                      The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        :return:
        """

        derivations = src.analytics.derivations.Derivations(cases=cases).exc()
        derivations.reset_index(drop=False, inplace=True)
        derivations.rename(columns={'index': 'tag'}, inplace=True)

        return derivations

    def exc(self) -> str:
        """

        :return:
        """

        logging.info('The best model, named by architecture: %s', self.__architecture)

        # Limits
        limits: lm.Limits = src.analytics.limits.Limits(s3_parameters=self.__s3_parameters).exc()

        # The boundaries array is a (1 X 2) vector
        boundaries: np.ndarray = limits.dispatches.product(axis=1).values[None, ...]
        numbers = limits.frequencies.copy()
        numbers['minimum'] = boundaries.min() * numbers['minimum']
        numbers['maximum'] = boundaries.min() * numbers['maximum']

        # The error matrix frequencies of a case/category, and their error metrics
        # derivations.  Additionally, a category column.
        cases = self.__cases()
        derivations = self.__derivations(cases=cases)
        derivations = derivations.assign(category=derivations['tag'].map(self.__configurations.categories))

        # Spiders
        src.analytics.spider.Spider().exc(blob=derivations)
        src.analytics.bullet.Bullet(error=limits.error).exc(blob=derivations)
        src.analytics.cost.Cost(costs=limits.costs, numbers=numbers).exc()

        return self.__architecture
