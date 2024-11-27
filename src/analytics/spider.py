import logging

import pandas as pd


class Spider:

    def __init__(self):

        self.__names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                 'fscore': 'F Score', 'youden': "Youden's J Statistic", 'balanced_accuracy': 'Balanced Accuracy',
                 'standard_accuracy': 'Standard Accuracy'}

    def exc(self, blob: pd.DataFrame):

        derivations = blob.copy()

        categories = derivations['category'].unique()

        # The tag & category values are required for data structuring
        derivations.set_index(keys=['tag', 'category'], drop=False, inplace=True)

        # Hence
        for category in categories:

            excerpt: pd.DataFrame = derivations.loc[derivations['category'] == category, self.__names.keys()]
            logging.info(excerpt)

            excerpt.rename(columns=self.__names, inplace=True)

            dictionary = excerpt.to_dict(orient='tight')
            logging.info(dictionary)
