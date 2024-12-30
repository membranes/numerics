"""Module interface.py"""
import pandas as pd

import src.abstracts.distributions


class Interface:
    """
    The interface to the data package's classes
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def exc(architecture: str, tags: pd.DataFrame):
        """

        :param architecture:
        :param tags:
        :return:
        """

        # Distributions of tags.
        src.abstracts.distributions.Distributions(architecture=architecture, tags=tags).exc()
