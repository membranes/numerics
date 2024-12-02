"""Module costs.py"""
import logging

import numpy as np
import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.analytics.limits


class Costs:

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Limits instance
        self.__limits = src.analytics.limits.Limits(s3_parameters=self.__s3_parameters)

        # Configurations
        self.__configurations = config.Config()

        # Rates
        self.__rates = np.linspace(start=0, stop=1, num=101)
        self.__rates = self.__rates[1:]
        self.__rates = self.__rates[..., None]

    def __fnr(self):
        pass

    def __fpr(self):
        pass

    def exc(self):

        # costs = pd.read_json(
        #     path_or_buf=f's3://{self.__s3_parameters.configurations}/limits/costs.json', orient='split')
        costs = self.__limits.exc(filename='costs.json', orient='split')
        logging.info(costs)

        # frequencies = pd.read_json(
        #     path_or_buf=f's3://{self.__s3_parameters.configurations}/limits/frequencies.json', orient='index')
        frequencies = self.__limits.exc(filename='frequencies.json', orient='index')
        logging.info(frequencies)

        categories = list(frequencies.index)

        for category in categories:

            cost: int = costs.loc['fnr', category]

            numbers = np.multiply(
                self.__rates, np.expand_dims(frequencies.loc[category, :].to_numpy(), axis=0))
            factors = cost * (1 + (numbers > 500).astype(int))
            liabilities = np.multiply(factors, numbers)

            data = pd.DataFrame(data=liabilities, columns=['min', 'max'])
            data = data.assign(rate=self.__rates)
            logging.info(data)
