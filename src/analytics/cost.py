"""Module cost.py"""
import logging
import os

import dask
import numpy as np
import pandas as pd

import config
import src.analytics.cost_false_negative_rate as cfn
import src.analytics.cost_false_positive_rate as cfp
import src.functions.objects


class Cost:
    """
    Class Costs
    """

    def __init__(self, costs: pd.DataFrame, frequencies: pd.DataFrame):
        """

        :param costs
        :param frequencies
        """

        self.__costs = costs
        self.__frequencies = frequencies

        # Configurations
        self.__configurations = config.Config()
        self.__objects = src.functions.objects.Objects()

        # Rates, self.__rates: np.ndarray = self.__rates[..., None]
        self.__rates: np.ndarray = np.linspace(start=0, stop=1, num=101)
        self.__rates: np.ndarray = (self.__rates[1:])[..., None]

        # Instances
        self.__cfn = cfn.CostFalseNegativeRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)
        self.__cfp = cfp.CostFalsePositiveRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)

    @dask.delayed
    def __fnr(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        # item = cfn.CostFalseNegativeRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)

        return self.__cfn.exc(category=category)

    @dask.delayed
    def __fpr(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        # item = cfp.CostFalsePositiveRate(rates=self.__rates, costs=self.__costs, frequencies=self.__frequencies)

        return self.__cfp.exc(category=category)

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

        categories = list(self.__frequencies.index)
        computations = []
        for category in categories:

            fnr = self.__fnr(category=category)
            _fnr = self.__persist(nodes=fnr, metric='fnr', category=category)
            fpr = self.__fpr(category=category)
            _fpr = self.__persist(nodes=fpr, metric='fpr', category=category)

            computations.append([_fnr, _fpr])

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
