"""Module cost_false_positive_rate.py"""
import numpy as np
import pandas as pd


class CostFalsePositiveRate:
    """
    False Positive Rate Cost
    """

    def __init__(self, rates: np.ndarray, costs: pd.DataFrame, frequencies: pd.DataFrame):
        """

        :param rates:
        :param costs:
        :param frequencies:
        """

        self.__rates = rates
        self.__costs = costs
        self.__frequencies = frequencies

    def __estimates_fpr(self, cost: int, boundaries: pd.DataFrame) -> np.ndarray:
        """

        :param cost:
        :param boundaries:
        :return:
        """

        numbers: np.ndarray = np.multiply(self.__rates, np.expand_dims(boundaries.to_numpy(), axis=0))
        liabilities: np.ndarray = cost * numbers
        estimates = np.concat((self.__rates, liabilities), axis=1)

        return estimates

    @staticmethod
    def __nodes(estimates: np.ndarray) -> dict:
        """

        :param estimates:
        :return:
        """

        # x: rate, low: ~ minimum cost, high: ~ maximum cost
        data = pd.DataFrame(data=estimates, columns=['x', 'low', 'high'])
        nodes = data.to_dict(orient='tight')

        return nodes

    def exc(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        # False Negative Rate Cost per Category
        cost: int = self.__costs.loc['fpr', category]

        # The approximate minimum & maximum ...
        boundaries = self.__frequencies.loc[category, :]

        # Hence
        estimates = self.__estimates_fpr(cost=cost, boundaries=boundaries)
        nodes = self.__nodes(estimates=estimates)
        nodes['cost'] = int(cost)
        nodes['approximate_annual_frequencies'] = boundaries.to_numpy().tolist()

        return nodes
