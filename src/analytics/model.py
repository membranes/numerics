"""Module model.py"""
import logging
import os

import pandas as pd

import config
import src.analytics.derivations
import src.data.architecture
import src.elements.model as bs
import src.functions.objects


class Best:
    """
    Determines the best model
    """

    def __init__(self):
        """
        Constructor
        """

        # Configurations
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

    def exc(self, tags: pd.DataFrame) -> bs.Model:
        """

        :param tags: A data frame summarising the projects tags, alongside each tag's annotation and category details.
        :return:
        """

        # A category column.
        values = tags[['tag', 'category']].set_index(keys='tag').to_dict(orient='dict')

        # The error matrix frequencies per case/category; and their error metrics derivations.
        cases = self.__cases()
        derivations = self.__derivations(cases=cases)
        derivations = derivations.assign(category=derivations['tag'].map(values['category']))

        return bs.Model(architecture=self.__architecture, derivations=derivations)
