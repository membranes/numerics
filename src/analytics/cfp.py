"""Module cfp.py"""
import numpy as np
import pandas as pd


class CFP:
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

    def __estimates_fpr(self, cost: int, boundaries: np.ndarray) -> np.ndarray:
        """

        :param cost:
        :param boundaries:
        :return:
        """

        numbers: np.ndarray = np.multiply(self.__rates, np.expand_dims(boundaries, axis=0))
        liabilities: np.ndarray = cost * numbers
        estimates = np.concat((self.__rates, liabilities), axis=1)

        return estimates

    def exc(self, category: str) -> dict:
        """

        :param category:
        :return:
        """

        # False Positive Rate Cost per Category
        cost = self.__costs.loc['fpr', category]

        # The approximate minimum & maximum ...
        boundaries = self.__frequencies.loc[category, :].to_numpy()

        # Hence
        estimates = self.__estimates_fpr(cost=cost, boundaries=boundaries)

        # Nodes
        nodes = pd.DataFrame(data=estimates, columns=['x', 'low', 'high']).to_dict(orient='tight')
        nodes['cost'] = int(cost)
        nodes['approximate_annual_frequencies'] = boundaries.tolist()

        return nodes
