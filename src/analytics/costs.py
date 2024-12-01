
import logging

import pandas as pd
import numpy as np

import config
import src.elements.service as sr
import src.elements.s3_parameters as s3p


class Costs:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()

        self.__rates = np.linspace(start=0, stop=1, num=101)
        self.__rates = self.__rates[1:]

    def __fnr(self):
        pass

    def exc(self):

        costs = pd.read_json(
            path_or_buf=f's3://{self.__s3_parameters.configurations}/limits/costs.json', orient='split')
        logging.info(costs)

        frequencies = pd.read_json(
            path_or_buf=f's3://{self.__s3_parameters.configurations}/limits/frequencies.json', orient='index')
        logging.info(frequencies)
