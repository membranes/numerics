"""Module text.py"""
import collections
import logging
import os
import pathlib

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

    def __init__(self, architecture: str, tags: pd.DataFrame):
        """

        :param architecture:
        :param tags:
        """

        self.__architecture = architecture
        self.__tags = tags

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __data(self, uri: str) -> pd.DataFrame:
        """

        :return:
        """

        text = src.elements.text_attributes.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    @staticmethod
    def __string(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        frame = data.copy()
        frame['string'] = frame['sentence'].str.split().map(','.join)

        return frame

    @staticmethod
    def __elements(instance: pd.Series, codes: list[int]) -> str:
        """

        :param instance: The parts are 'sentence' & 'code_per_tag'
        :param codes:
        :return:
        """

        frame = pd.DataFrame(
            data={'element': instance['sentence'].split(maxsplit=-1),
                  'code': instance['code_per_tag'].split(',', maxsplit=-1)})
        frame['code'] = frame['code'].astype(dtype=int)

        # The elements associated with the tags in focus
        frame: pd.DataFrame = frame.copy().loc[frame['code'].isin(codes), :]
        elements = ','.join(frame['element'].to_list())

        return elements

    def __persist(self, nodes: dict, name: str) -> str:
        """

        :param nodes: The strings cloud drawing data, as structurally required.
        :param name:
        :return:
        """

        return src.functions.objects.Objects().write(
            nodes=nodes,
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name}.json'))

    def exc(self, uri_: list[str], codes: list[int]):
        """

        :return:
        """

        for uri in uri_:

            stem = pathlib.Path(uri).stem
            data: pd.DataFrame = self.__data(uri=uri)
            data: pd.DataFrame = self.__string(data=data)
            data['elements'] = data[['sentence', 'code_per_tag']].apply(self.__elements, codes=codes, axis=1)

            frequencies = data['elements'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()

            logging.info('%s\n%s', stem, dict(frequencies))
