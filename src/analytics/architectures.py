import logging

import numpy as np

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Architectures:
    """
    The artefacts per architecture
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        self.__prefix = self.__s3_parameters.path_internal_artefacts

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __keys(self) -> list:
        """

        :return:
        """

        listings: list = src.s3.prefix.Prefix(
            service=self.__service, bucket_name=self.__s3_parameters.internal).objects(prefix=self.__prefix)

        return listings

    @staticmethod
    def __excerpt(keys: list) -> list:
        """
        Extracts the keys within prime/model directory

        :param keys:
        :return:
        """

        listings: list = [k for k in keys if k.__contains__('/prime/model')]

        return listings

    def exc(self):
        """

        :return:
        """

        # Determining the unique list of fine-tuned models
        keys = self.__keys()
        excerpt = self.__excerpt(keys=keys)

        return excerpt
