import os
import logging

import pandas as pd
import numpy as np

import config
import src.analytics.limits
import src.elements.service as sr
import src.elements.s3_parameters as s3p


class Costs:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__configurations = config.Config()

        self.__rates = np.linspace(start=0, stop=1, num=101)
        self.__rates = self.__rates[1:]

        self.__limits = src.analytics.limits.Limits(service=service, s3_parameters=s3_parameters)

    def __fnr(self):
        pass

    def exc(self):

        _costs = self.__limits.exc(key_name='limits/costs.json')
        logging.info(_costs)

        _frequencies = self.__limits.exc(key_name='limits/frequencies.json')
        logging.info(_frequencies)
