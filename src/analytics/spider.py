"""Module spider.py"""
import logging
import os

import pandas as pd

import config
import src.functions.directories
import src.functions.objects


class Spider:
    """
    Class Spider
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # The directory wherein the data files, for the spider graphs, are stored.
        self.__path = os.path.join(self.__configurations.card_, 'spider')
        src.functions.directories.Directories().create(path=self.__path)

        # An instance for reading & writing JSON (JavaScript Object Notation) files.
        self.__objects = src.functions.objects.Objects()

        # The metrics in focus.
        self.__names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                        'fscore': 'F Score', 'balanced_accuracy': 'Balanced Accuracy',
                        'standard_accuracy': 'Standard Accuracy'}

    def __save(self, nodes: dict, name: str):
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
        derivations.set_index(keys=['tag', 'category'], drop=False, inplace=True)

        # Hence
        for category in categories:

            name = self.__configurations.definition[category]
            logging.info(name)

            # The instances of the category
            excerpt: pd.DataFrame = derivations.loc[derivations['category'] == category, self.__names.keys()]
            excerpt.rename(columns=self.__names, inplace=True)

            # The dictionary of the instances
            nodes = excerpt.to_dict(orient='tight')
            logging.info(nodes)

            # Save
            message = self.__save(nodes=nodes, name=f'{name}.json')
            logging.info(message)
