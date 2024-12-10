"""Module artefacts.py"""
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

    def __strings(self, sources: np.ndarray):
        """

        :param sources: An array of Amazon S3 (Simple Storage Service) prefixes
        :return:
        """

        # A data frame consisting of the S3 keys ...
        frame = pd.DataFrame(data={'source': sources})

        # ... and local storage area.  For the local storage area, ensure that the
        # appropriate directory separator is in place.
        frame = frame.assign(destination=frame['source'])
        frame = frame.assign(destination=frame['destination'].replace(to_replace='/', value=os.path.sep))
        frame = frame.assign(destination=self.__configurations.data_ + os.path.sep + frame['destination'])

        return frame

    def exc(self) -> pd.DataFrame:
        """
        Determining the unique segments of fine-tuned models

        :return:
        """

        # The keys within the <artefacts> prefix
        keys = self.__keys()

        # Focusing on the keys within the model & metrics paths
        keys = self.__excerpt(keys=keys)

        # Hence, the distinct model & metrics sources/paths
        sources = np.array([os.path.dirname(k) for k in keys])
        sources = np.unique(sources)
        self.__logger.info(sources)

        # Source & Destination
        strings = self.__strings(sources=sources)
        self.__logger.info(strings)

        return strings
