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

        src.analytics.estimates.Estimates(architecture=architecture).exc()
