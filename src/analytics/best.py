
import typing
import logging
import os
import pandas as pd

import config
import src.data.architecture
import src.elements.best as bs
import src.functions.objects
import src.analytics.derivations


class Best:
    """
    Determines the best model
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # The architecture name of the best model, ...
        self.__architecture: str = src.data.architecture.Architecture().exc()
        logging.info('The best model, named by architecture: %s', self.__architecture)

    def __cases(self) -> pd.DataFrame:
        """

        :return: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                 The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        """

        path = os.path.join(
            self.__configurations.artefacts_, self.__architecture, self.__configurations.branch)
        cases = src.functions.objects.Objects().frame(path=path, orient='index')

        return cases

    @staticmethod
    def __derivations(cases: pd.DataFrame) -> pd.DataFrame:
        """
        Appends a series of metrics to each instance.

        :param cases: Each instance represents a distinct tag; tag = annotation &#x29FA; category.
                      The frame must include the error matrix frequencies is tp, tn, fp, & fn.
        :return:
        """

        derivations = src.analytics.derivations.Derivations(cases=cases).exc()
        derivations.reset_index(drop=False, inplace=True)
        derivations.rename(columns={'index': 'tag'}, inplace=True)
        derivations['tag'] = derivations['tag'].str.upper()

        return derivations

    def exc(self) -> bs.Best:
        """

        :return:
        """

        # The error matrix frequencies of a case/category
        cases = self.__cases()

        # ... and their error metrics derivations.
        derivations = self.__derivations(cases=cases)

        # A category column.
        derivations = derivations.assign(category=derivations['tag'].map(self.__configurations.categories))

        return bs.Best(architecture=self.__architecture, derivations=derivations)
