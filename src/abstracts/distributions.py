"""Module distributions.py"""
import logging
import collections
import os
import glob

import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Distributions:
    """
    Class Distributions
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

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def __frequencies(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # Tags: tag/annotation/annotation_name/category/category_name
        descriptions = self.__tags[['tag', 'name']].set_index('tag').to_dict()['name']

        # The frequencies
        frequencies = data['tagstr'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()
        items = [[k, frequencies[k], descriptions[k]] for k, v in frequencies.items()]

        # Hence
        frame = pd.DataFrame(data=items, columns=['tag', 'frequency', 'name'])
        frame.rename(columns={'tag': 'id', 'frequency': 'value'}, inplace=True)

        return frame

    def __persist(self, blob: pd.DataFrame, name: str):
        """
        For drawing a tree.

        :param blob: The drawing data, being saved as structurally required
        :param name:
        :return:
        """

        nodes = blob.to_dict(orient='dict')

        src.functions.objects.Objects().write(
            nodes=nodes,
            path=os.path.join(self.__configurations.numerics_, 'abstracts', f'{name }.json'))

    def exc(self):
        """

        :return:
        """

        # The data
        uri_ = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, self.__architecture, 'data', '*.csv'))
        logging.info(uri_)

        computation = []
        for uri in uri_:

            data = self.__data(uri=uri)

            frequencies = self.__frequencies(data=data)

            computation.append(frequencies.to_dict(orient='tight'))
