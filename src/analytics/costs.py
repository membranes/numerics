"""Module costs.py"""
import logging
import os

import dask
import numpy as np
import pandas as pd

import config
import src.analytics.limits
import src.elements.s3_parameters as s3p
import src.functions.objects


class Costs:
    """
    Class Costs
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Limits instance
        self.__limits = src.analytics.limits.Limits(s3_parameters=self.__s3_parameters)
        self.__costs = self.__limits.exc(filename='costs.json', orient='split')
        self.__frequencies = self.__limits.exc(filename='frequencies.json', orient='index')

        # Rates
        self.__rates = np.linspace(start=0, stop=1, num=101)
        self.__rates = self.__rates[1:]
        self.__rates = self.__rates[..., None]

    @dask.delayed
    def __fnr(self, category: str) -> np.ndarray:
        """

        :param category:
        :return:
        """

        n_inflection = 500

        cost: int = self.__costs.loc['fnr', category]
        numbers = np.multiply(self.__rates,
                              np.expand_dims(self.__frequencies.loc[category, :].to_numpy(), axis=0))
        factors = cost * (1 + 0.5*(numbers > n_inflection).astype(int))
        liabilities = np.multiply(factors, numbers)
        matrix = np.concat((self.__rates, liabilities), axis=1)

        return matrix

    @dask.delayed
    def __fpr(self, category: str) -> np.ndarray:
        """

        :param category:
        :return:
        """

        cost: int = self.__costs.loc['fpr', category]
        numbers = np.multiply(self.__rates,
                              np.expand_dims(self.__frequencies.loc[category, :].to_numpy(), axis=0))
        liabilities = cost * numbers
        matrix = np.concat((self.__rates, liabilities), axis=1)

        return matrix

    @dask.delayed
    def __persist(self, matrix: np.ndarray, metric: str, category: str) -> str:
        """

        :param matrix: Fields rate, ~ minimum cost, ~ maximum cost
        :param metric: fnr (false negative rate) or fpr (false positive rate)
        :param category: Category code, e.g., GEO, GPE, etc. (ref. self.definition in config.py)
        :return:
        """

        # The file name, and path; path = directory + file name
        name = f'{self.__configurations.definition[category]}.json'
        path = os.path.join(self.__configurations.numerics_, 'cost', metric, name)

        # x: rate, low: ~ minimum cost, high: ~ maximum cost
        data = pd.DataFrame(data=matrix, columns=['x', 'low', 'high'])
        nodes = data.to_dict(orient='tight')

        return self.__objects.write(nodes=nodes, path=path)

    def exc(self):
        """

        :return:
        """

        categories = list(self.__frequencies.index)

        computations = []
        for category in categories:

            fnr = self.__fnr(category=category)
            message_fnr = self.__persist(matrix=fnr, metric='fnr', category=category)

            fpr = self.__fpr(category=category)
            message_fpr = self.__persist(matrix=fpr, metric='fpr', category=category)

            computations.append([message_fnr, message_fpr])

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
