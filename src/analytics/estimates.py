import config
import logging
import os

import pandas as pd


class Estimates:

    def __init__(self, architecture: str):
        """

        :param architecture:
        """

        self.__architecture = architecture

        # Configurations
        self.__configurations = config.Config()

    def __cases(self):

        path = os.path.join(self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)

        try:
            cases = pd.read_json(path_or_buf=path, orient='index')
        except ImportError as err:
            raise err from err

        return cases

    def exc(self):

        cases = self.__cases()
        logging.info(cases)
