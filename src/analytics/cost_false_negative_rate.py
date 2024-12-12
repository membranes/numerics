"""Module cost_false_negative.py"""
import numpy as np
import pandas as pd


class CostFalseNegativeRate:
    """
    False Negative Rate Cost
    """

    def __init__(self, rates: np.ndarray, costs: pd.DataFrame, frequencies: pd.DataFrame):
        """

        :param rates: An array of false negative rate values; (0, 1]<br>
        :param costs: A dataframe of cost per category, and per rate type
              <ul>
                <li>Categories: Of this project &rarr; <b>GEO</b>: geographic, <b>GPE</b>: geopolitical,
                    <b>ORG</b>: organisation, <b>PER</b>: person, <b>TIM</b>: time, <b>O</b>: miscellaneous</li>
                <li>Rate Types: false negative rate (fnr), false positive rate (fpr)</li>
              </ul><br>
        :param frequencies:  Per category, and per annum, it summarises the approximate minimum & maximum expected
                             occurrences of words in the category.<br>
        """

        self.__rates = rates
        self.__costs = costs
        self.__frequencies = frequencies

    def __estimates(self, cost: int, boundaries: pd.DataFrame) -> np.ndarray:
        """

        :param cost:
        :param boundaries:
        :return:
        """

        n_inflection = 500

        # Possible missed classifications range per rate value of a static annual frequency range
        numbers = np.multiply(
            self.__rates, np.expand_dims(boundaries.to_numpy(), axis=0))

        # Hence
        factors = cost * (1 + 0.5*(numbers > n_inflection).astype(int))
        liabilities = np.multiply(factors, numbers)
        estimates = np.concat((self.__rates, liabilities), axis=1)

        return estimates

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

    def exc(self, category: str):
        """

        :param category:
        :return:
        """

        cost: int = self.__costs.loc['fnr', category]
        boundaries: pd.DataFrame = self.__frequencies.loc[category, :]

        estimates = self.__estimates(cost=cost, boundaries=boundaries)
        nodes = self.__nodes(estimates=estimates)

        nodes['cost'] = cost
        nodes['approximate_annual_frequencies'] = boundaries

        return nodes
