import logging
import glob
import os

import config
import src.transfer.dictionary
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.directories
import src.s3.ingress


class Interface:

    def __init__(self, service: sr.Service,  s3_parameters: s3p):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Instances
        self.__configurations = config.Config()
        self.__dictionary = src.transfer.dictionary.Dictionary()

    def exc(self):

        strings = self.__dictionary.exc(
            path=os.path.join(os.getcwd(), 'warehouse'), extension='json', prefix='warehouse')

        # Transfer
        messages = src.s3.ingress.Ingress(
            service=self.__service, bucket_name=self.__s3_parameters.external).exc(strings=strings)
        logging.info(messages)
