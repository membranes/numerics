"""Module bullet.py"""
import logging
import os

import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Bullet:
    """
    Description<br>
    ------------<br>
    Prepares the data for the <b>False Negative Rate</b> & <b>False Positive Rate</b> bullet graphs.
    """

    def __init__(self, error: pd.DataFrame):
        """

        :param
        """

        # The metrics in focus.
        self.__names = {'fnr': 'False Negative Rate', 'fpr': 'False Positive Rate'}

        # Hence, error values
        error = error[self.__names.keys()]
        error.rename(columns=self.__names, inplace=True)
        self.__error = error

        # Configurations.  The directory wherein the data files, for the spider graphs, are stored.
        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.numerics_, 'card', 'bullet')

        # An instance for reading & writing JSON (JavaScript Object Notation) files.
        self.__objects = src.functions.objects.Objects()

    def __save(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The dictionary of values for the spider graph
        :param name: The name of the file; filename & extension.
        :return:
        """

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, name))

        return message

    def exc(self, blob: pd.DataFrame):
        """

        :param blob: A data frame consisting of error matrix frequencies & metrics, alongside
                     tags & categories identifiers.
        :return:
        """

        derivations = blob.copy()

        # The unique tag categories
        categories = derivations['category'].unique()

        # The tag & category values are required for data structuring
        derivations.set_index(keys=['tag'], drop=False, inplace=True)

        # Hence
        for category in categories:

            name = self.__configurations.definition[category]

            # The instances of the category
            excerpt: pd.DataFrame = derivations.loc[derivations['category'] == category, self.__names.keys()]
            excerpt.rename(columns=self.__names, inplace=True)

            # The dictionary of the instances
            nodes = excerpt.to_dict(orient='split')
            nodes['target'] = self.__error.loc[category, nodes['columns']].to_list()

            # Save
            message = self.__save(nodes=nodes, name=f'{name}.json')
            logging.info(message)
