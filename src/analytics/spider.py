
import pandas as pd


class Spider:

    def __init__(self, blob: pd.DataFrame):

        self.__blob = blob

        names = {'precision': "Precision", 'sensitivity': "Sensitivity", 'specificity': 'Specificity',
                 'fscore': 'F Score', 'youden': "Youden's JJ Statistic", 'balanced_accuracy': 'Balanced Accuracy',
                 'standard_accuracy': 'Standard Accuracy'}

    def exc(self):
        pass
