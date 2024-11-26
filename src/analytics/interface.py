"""Module interface.py"""
import logging

import src.analytics.architecture


class Interface:

    def __init__(self):
        pass

    def exc(self):
        """

        :return:
        """

        message = src.analytics.architecture.Architecture().exc()

        logging.info(message)
