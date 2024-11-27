"""Module estimates.py"""
import logging
import os

import pandas as pd

import config
import src.analytics.derivations
import src.analytics.spider


class Estimates:
    """
    For estimating/calculating a variety of metrics.
    """

    def __init__(self, architecture: str):
        """

        :param architecture: The best architecture
        """

        self.__architecture = architecture

        # Configurations
        self.__configurations = config.Config()

    def __cases(self):
        """

        :return: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                 The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        """

        path = os.path.join(self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)

        try:
            cases = pd.read_json(path_or_buf=path, orient='index')
        except ImportError as err:
            raise err from err

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

    def exc(self):
        """

        :return:
        """

        cases = self.__cases()
        derivations = self.__derivations(cases=cases)

        # Add a category column
        derivations = derivations.assign(category=derivations['tag'].map(self.__configurations.categories))
        logging.info(derivations)

        # Spiders
        src.analytics.spider.Spider().exc(blob=derivations)
