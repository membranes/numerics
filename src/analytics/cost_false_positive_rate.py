
import numpy as np
import pandas as pd


class CostFalsePositiveRate:

    def __init__(self, rates: np.ndarray, costs: pd.DataFrame, frequencies: pd.DataFrame):
        """

        :param rates:
        :param costs:
        :param frequencies:
        """

        self.__rates = rates
        self.__costs = costs
        self.__frequencies = frequencies

    def __estimates(self, cost: int, boundaries: pd.DataFrame):
        """

        :param cost:
        :param boundaries:
        :return:
        """

        numbers = np.multiply(self.__rates,
                              np.expand_dims(boundaries.to_numpy(), axis=0))
        liabilities = cost * numbers
        matrix = np.concat((self.__rates, liabilities), axis=1)

        return matrix

    @staticmethod
    def __nodes(estimates: np.ndarray):
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

        cost: int = self.__costs.loc['fpr', category]
        boundaries = self.__frequencies.loc[category, :]

        estimates = self.__estimates(cost=cost, boundaries=boundaries)
        nodes = self.__nodes(estimates=estimates)
        nodes['cost'] = cost
        nodes['approximate_annual_frequencies'] = boundaries.to_numpy().tolist()

        return nodes
