"""Module cost.py"""
import logging
import os

import dask
import numpy as np
import pandas as pd

import config
import src.analytics.limits
import src.elements.s3_parameters as s3p
import src.functions.objects
import src.analytics.cost_false_negative_rate as cfn
import src.analytics.cost_false_positive_rate as cfp


class Cost:
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
        self.__costs: pd.DataFrame = self.__limits.exc(filename='costs.json', orient='split')
        self.__frequencies: pd.DataFrame = self.__limits.exc(filename='frequencies.json', orient='index')

        # Rates
        self.__rates: np.ndarray = np.linspace(start=0, stop=1, num=101)
        self.__rates: np.ndarray = self.__rates[1:]
        self.__rates: np.ndarray = self.__rates[..., None]

    @dask.delayed
    def __fnr(self, category: str) -> np.ndarray:
        """

        :param category:
        :return:
        """

    @dask.delayed
    def __fpr(self, category: str) -> np.ndarray:
        """

        :param category:
        :return:
        """

    @dask.delayed
    def __persist(self, nodes: dict, metric: str, category: str) -> str:
        """

        :param nodes: The graph data.
        :param metric: fnr (false negative rate) or fpr (false positive rate)
        :param category: Category code, e.g., GEO, GPE, etc. (ref. self.definition in config.py)
        :return:
        """

        # The file name, and path; path = directory + file name
        name = f'{self.__configurations.definition[category]}.json'
        path = os.path.join(self.__configurations.numerics_, 'cost', metric, name)

        return self.__objects.write(nodes=nodes, path=path)

    def exc(self):
        """

        :return:
        """

        _fnr = cfn.CostFalseNegativeRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)
        _fpr = cfp.CostFalsePositiveRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)

        categories = list(self.__frequencies.index)
        computations = []
        for category in categories:

            # fnr = self.__fnr(category=category)
            fnr = dask.delayed(_fnr)(category)
            message_fnr = self.__persist(matrix=fnr, metric='fnr', category=category)

            # fpr = self.__fpr(category=category)
            fpr = dask.delayed(_fpr)(category)

            message_fpr = self.__persist(matrix=fpr, metric='fpr', category=category)

            computations.append([message_fnr, message_fpr])

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
