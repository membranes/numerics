"""Module """
import glob
import logging
import os

import pandas as pd

import config
import src.analytics.derivations
import src.functions.objects


class Architecture:
    """
    <b>Class Architecture</b><br>
    -------------------<br>

    Selects the best architecture, i.e., the best model.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        self.__objects = src.functions.objects.Objects()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __cases(self, tree: str) -> pd.DataFrame:
        """

        :param tree:
        :return:
        """

        path = os.path.join(tree, self.__configurations.branch)
        cases = self.__objects.frame(path=path, orient='index')

        return cases

    @staticmethod
    def __median_mcc(cases: pd.DataFrame) -> float:
        """

        :param cases: Each instance represents a distinct tag; tag = annotation &#x29FA; category.<br>
        :return:
        """

        matthews: pd.Series = src.analytics.derivations.Derivations(cases=cases).matthews()

        return matthews.median()

    def __best(self, data: pd.DataFrame) -> str:
        """

        :param data: Whence the best is selected from.
        :return:
        """

        selection: pd.Series = data.copy().loc[data['median'].idxmax(), :]

        self.__logger.info('Best:\n%s', selection)

        return selection['architecture']

    def __save(self, best: str):
        """

        :param best:
        :return:
        """

        path = os.path.join(self.__configurations.numerics_, 'best', 'architecture.json')
        message = self.__objects.write(nodes={'name': best}, path=path)

        self.__logger.info(message)


    def exc(self) -> str:
        """

        :return:
        """

        # The directories within the self.__configurations.artefacts_ directory.  Each directory
        # represents an architecture.
        trees = glob.glob(os.path.join(self.__configurations.artefacts_, '*'), recursive=False)

        # Each tree/architecture has a testing/fundamental.json dictionary
        computations = []
        for tree in trees:
            cases = self.__cases(tree=tree)
            values = {"median": self.__median_mcc(cases=cases),
                      "architecture": os.path.basename(tree)}
            computations.append(values)

        data = pd.DataFrame.from_records(computations)
        best = self.__best(data=data)

        self.__save(best=best)

        return best
