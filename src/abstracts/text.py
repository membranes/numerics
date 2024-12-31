"""Module text.py"""
import logging
import os

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.text_attributes
import src.functions.objects
import src.functions.streams


class Text:
    """
    Schema
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        # Configurations
        self.__configurations = config.Config()

        # The data file
        self.__filepath = f"s3://{s3_parameters.configurations}/projects/schema.csv"

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __read(self) -> pd.DataFrame:
        """

        :return:
        """

        text = src.elements.text_attributes.TextAttributes(uri=self.__filepath, header=0)

        return src.functions.streams.Streams().api(text=text)

    def __persist(self, blob: pd.DataFrame, name: str) -> str:
        """
        For drawing a network graph of the project scoping schema

        :param blob: The drawing data, being saved as structurally required.
        :param name:
        :return:
        """

        return src.functions.objects.Objects().write(
            nodes=blob.to_dict(orient='tight'),
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name}.json'))

    def exc(self):
        """

        :return:
        """

        # The data
        data: pd.DataFrame = self.__read()
        self.__logger.info(data.head())

        # Dictionary
        message = self.__persist(blob=data, name='schema')
        self.__logger.info(message)
