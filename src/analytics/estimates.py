"""Module estimates.py"""
import logging
import os

import pandas as pd

import config
import src.analytics.derivations


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

        :return:
        """

        path = os.path.join(self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)

        try:
            cases = pd.read_json(path_or_buf=path, orient='index')
        except ImportError as err:
            raise err from err

        return cases

    def exc(self):
        """

        :return:
        """

        cases = self.__cases()
        derivations = src.analytics.derivations.Derivations(cases=cases).exc()
        logging.info(derivations)
