"""Module interface.py"""
import logging

import numpy as np
import pandas as pd

import config
import src.analytics.bullet
import src.analytics.cost
import src.analytics.derivations
import src.analytics.spider
import src.data.limits
import src.elements.limits as lm
import src.elements.s3_parameters as s3p
import src.functions.directories


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

    def __storage(self):
        """
        Creates all the paths for the graphing & serving data.

        :return:
        """

        directories = src.functions.directories.Directories()

        for value in self.__configurations.graphs_:
            directories.create(value)

    @staticmethod
    def __numbers(limits: lm.Limits):
        """

        :param limits:
        :return:
        """

        # The boundaries array is a (1 X 2) vector
        boundaries: np.ndarray = limits.dispatches.product(axis=1).values[None, ...]
        numbers = limits.frequencies.copy()
        numbers['minimum'] = boundaries.min() * numbers['minimum']
        numbers['maximum'] = boundaries.min() * numbers['maximum']

        return numbers

    def exc(self, derivations: pd.DataFrame) -> None:
        """

        :param derivations:
        :return:
        """

        # Limits
        limits: lm.Limits = src.data.limits.Limits(s3_parameters=self.__s3_parameters).exc()

        # Numbers
        numbers = self.__numbers(limits=limits)

        # Spiders
        src.analytics.spider.Spider().exc(blob=derivations)
        src.analytics.bullet.Bullet(error=limits.error).exc(blob=derivations)
        src.analytics.cost.Cost(costs=limits.costs, numbers=numbers).exc()
