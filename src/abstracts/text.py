"""Module text.py"""
import logging
import os
import glob

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes
import src.functions.objects
import src.functions.streams


class Text:
    """
    Text
    """

    def __init__(self, architecture: str):
        """

        :param architecture:
        """

        self.__architecture = architecture

        # Configurations
        self.__configurations = config.Config()



        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __data(self, uri: str) -> pd.DataFrame:
        """

        :return:
        """

        text = src.elements.text_attributes.TextAttributes(uri=uri, header=0)

        return src.functions.streams.Streams().api(text=text)

    def __string(self, data: pd.DataFrame, focus: str):
        pass


    def __persist(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The strings cloud drawing data, as structurally required.
        :param name:
        :return:
        """

        return src.functions.objects.Objects().write(
            nodes=nodes,
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name}.json'))

    def exc(self, uri_: list):
        """

        :return:
        """

        for uri in uri_:

            data: pd.DataFrame = self.__data(uri=uri)
            self.__logger.info(data.head())


