import logging
import os

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import config
import src.analytics.architectures


class Interface:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)30d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """
        os.path.join(configurations.artefacts_, 'distil', 'prime', 'model')

        :return:
        """

        strings: pd.DataFrame = src.analytics.architectures.Architectures(
            service=self.__service, s3_parameters=self.__s3_parameters).exc()

        self.__logger.info(strings)
