import logging
import os

import pandas as pd

import config
import src.functions.objects
import src.functions.directories


class Spider:

    def __init__(self):

        self.__configurations = config.Config()

        # The directory
        self.__path = os.path.join(self.__configurations.card_, 'spider')
        src.functions.directories.Directories().create(path=self.__path)

        # JSON
        self.__objects = src.functions.objects.Objects()

        # The metrics in focus
        self.__names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                 'fscore': 'F Score', 'youden': "Youden's J Statistic", 'balanced_accuracy': 'Balanced Accuracy',
                 'standard_accuracy': 'Standard Accuracy'}


    def __save(self, nodes: dict, name: str):
        """

        :param nodes:
        :param name:
        :return:
        """

        self.__objects.write(nodes=nodes, path=os.path.join(self.__path, name))

    def exc(self, blob: pd.DataFrame):

        derivations = blob.copy()

        # The unique tag categories
        categories = derivations['category'].unique()

        # The tag & category values are required for data structuring
        derivations.set_index(keys=['tag', 'category'], drop=False, inplace=True)

        # Hence
        for category in categories:

            excerpt: pd.DataFrame = derivations.loc[derivations['category'] == category, self.__names.keys()]
            excerpt.rename(columns=self.__names, inplace=True)

            name = self.__configurations.definition[category]
            logging.info(name)

            nodes = excerpt.to_dict(orient='tight')
            logging.info(nodes)

            self.__save(nodes=nodes, name=f'{name}.json')
