"""Module costs.py"""
import logging
import os
import collections

import numpy as np
import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.analytics.limits
import src.functions.objects


class Costs:

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

    def __fnr(self, category: str):

        cost: int = self.__costs.loc['fnr', category]

        numbers = np.multiply(
            self.__rates, np.expand_dims(self.__frequencies.loc[category, :].to_numpy(), axis=0))
        factors = cost * (1 + (numbers > 500).astype(int))
        liabilities = np.multiply(factors, numbers)
        matrix = np.concat((self.__rates, liabilities), axis=1)

        return matrix

    def __fpr(self, category: str):

        cost: int = self.__costs.loc['fpr', category]
        numbers = np.multiply(
            self.__rates, np.expand_dims(self.__frequencies.loc[category, :].to_numpy(), axis=0))
        liabilities = cost * numbers
        matrix = np.concat((self.__rates, liabilities), axis=1)

        return matrix

    def __persist(self, matrix: np.ndarray, metric: str, category: str):

        name = f'{self.__configurations.definition[category]}.json'
        path = os.path.join(self.__configurations.numerics_, 'cost', metric, name)

        data = pd.DataFrame(data=matrix, columns=['rate', 'min', 'max'])
        nodes = data.to_dict(orient='tight')

        self.__objects.write(nodes=nodes, path=path)

        # data.to_json(path_or_buf=path, orient='records', index=False)


    def exc(self):

        categories = list(self.__frequencies.index)

        for category in categories:

            fnr = self.__fnr(category=category)
            self.__persist(matrix=fnr, metric='fnr', category=category)
