"""Module interface.py"""
import logging

import src.analytics.architecture
import src.analytics.estimates


class Interface:

    def __init__(self):
        pass

    @staticmethod
    def exc():
        """

        :return:
        """

        architecture = src.analytics.architecture.Architecture().exc()
        logging.info(architecture)

        src.analytics.estimates.Estimates(architecture=architecture).exc()
