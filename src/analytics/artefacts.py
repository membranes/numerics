import logging
import os

import pandas as pd
import numpy as np

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Artefacts:
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

        self.__configurations = config.Config()
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

    def __excerpt(self, keys: list) -> list:
        """
        Extracts the keys within prime/model directory

        :param keys:
        :return:
        """

        listings: list = [k for k in keys if
                          k.__contains__(self.__configurations.prime_ + 'model') |
                          k.__contains__(self.__configurations.prime_ + 'metrics')]

        return listings

    def __strings(self, paths: np.ndarray):
        """

        :param keys: A list of Amazon S3 keys, i.e., prefix + vertex
        :return:
        """

        # A data frame consisting of the S3 keys ...
        frame = pd.DataFrame(data={'path': paths})

        # ... and local storage area.  For the local storage area, ensure that the
        # appropriate directory separator is in place.
        frame = frame.assign(destination=frame['path'])
        frame = frame.assign(destination=frame['destination'].replace(to_replace='/', value=os.path.sep))
        frame = frame.assign(destination=self.__configurations.data_ + os.path.sep + frame['destination'])

        return frame

    def exc(self):
        """

        :return:
        """

        # Determining the unique list of fine-tuned models
        keys = self.__keys()
        self.__logger.info(keys)

        # Focus
        keys = self.__excerpt(keys=keys)
        self.__logger.info(keys)

        paths = np.array([os.path.dirname(k) for k in keys])
        paths = np.unique(paths)
        self.__logger.info(paths)

        # Source & Destination
        strings = self.__strings(paths=paths)
        self.__logger.info(strings)

        return strings
