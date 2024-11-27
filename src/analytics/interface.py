"""Module interface.py"""
import logging

import config
import src.analytics.architecture
import src.analytics.estimates


class Interface:

    def __init__(self):

        self.__configurations = config.Config()

    def exc(self):
        """

        :return:
        """

        architecture = src.analytics.architecture.Architecture().exc()
        logging.info(architecture)

        estimates = src.analytics.estimates.Estimates(architecture=architecture).exc()
        estimates.reset_index(drop=False, inplace=True)
        logging.info(estimates)

        estimates = estimates.assign(category=estimates['index'].map(self.__configurations.categories))
        logging.info(estimates)
