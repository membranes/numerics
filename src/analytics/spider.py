import logging

import pandas as pd


class Spider:

    def __init__(self):

        self.__names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                 'fscore': 'F Score', 'youden': "Youden's JJ Statistic", 'balanced_accuracy': 'Balanced Accuracy',
                 'standard_accuracy': 'Standard Accuracy'}

    def exc(self, derivations: pd.DataFrame):

        categories = derivations['category'].unique()

        for category in categories:

            excerpt = derivations.loc[derivations['category'] == category, self.__names.keys()]
            logging.info(excerpt)
