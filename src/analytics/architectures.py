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

    def __keys(self):
        """

        :return:
        """

        listings: list = src.s3.prefix.Prefix(service=self.__service, bucket_name=self.__s3_parameters.internal).objects(
            prefix=self.__prefix)

        return listings

    def __names(self, keys: list):
        """

        :param keys:
        :return:
        """

        # Excluding the bucket prefix
        pathways = np.strings.replace(a=keys, old=self.__prefix, new='')

        # Next, determining the parent directories
        splittings = np.char.split(a=pathways, sep='/', maxsplit=1)
        objects = [splitting[0] for splitting in splittings]

        return np.unique(objects)

    def exc(self):
        """

        :return:
        """

        # The unique list of fine tuned models
        keys = self.__keys()
        names = self.__names(keys=keys)

        for name in names:

            self.__logger.info(f's3://{self.__s3_parameters.internal}/{self.__s3_parameters.path_internal_artefacts}{name}/prime/model')
