"""Module text.py"""
import logging
import os

import numpy as np
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

    def __init__(self, architecture: str, tags: pd.DataFrame, m_config: dict):
        """

        :param architecture:
        :param tags:
        :param m_config:
        """

        self.__architecture = architecture
        self.__tags = tags
        self.__m_config = m_config

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

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

        return self.__streams.read(text=text)

    @staticmethod
    def __string(data: pd.DataFrame) -> pd.DataFrame:

        frame = data.copy()

        frame['string'] = frame['sentence'].str.split().map(','.join)

        return frame

    @staticmethod
    def __elements(instance, code: int):

        frame = pd.DataFrame(
            data={'element': instance[0].split(maxsplit=-1),
                  'code': instance[1].split(',', maxsplit=-1)})
        frame['code'] = frame['code'].astype(dtype=int)
            
        logging.info(frame.loc[frame['code'] == code, :])

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
            data: pd.DataFrame = self.__string(data=data)
            np.apply_along_axis(func1d=self.__elements, axis=1, arr=data[['sentence', 'code_per_tag']], code=0)
