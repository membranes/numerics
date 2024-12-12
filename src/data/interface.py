"""Module interface.py"""
import logging

import pandas as pd

import src.data.artefacts
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.directives
import src.s3.egress


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)30d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """

        :return:
        """

        # Get the artefacts metadata
        strings: pd.DataFrame = src.data.artefacts.Artefacts(
            service=self.__service, s3_parameters=self.__s3_parameters).exc()
        self.__logger.info(strings)

        # Retrieve the artefacts
        message: bool = src.s3.directives.Directives(s3_parameters=self.__s3_parameters).exc(
            source=strings['source'], destination=strings['destination'])

        return message
