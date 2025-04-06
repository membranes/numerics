import collections
import glob
import logging
import os
import pathlib
import json

import pandas as pd

import config
import src.elements.text_attributes as txa
import src.functions.streams


class Bars:

    def __init__(self, tags: pd.DataFrame):

        self.__tags = tags

        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()


        # Graphing categories
        self.__categories = ['training', 'validating', 'testing']

    def __data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    def __frequencies(self, data: pd.DataFrame, stem: str):
        """

        :param data:
        :return:
        """

        # Tags: tag/annotation/annotation_name/category/category_name
        # descriptions = self.__tags[['tag', 'group']].set_index('tag').to_dict()['group']
        frequencies = data['tagstr'].str.upper().str.split(pat=',', n=-1, expand=False).map(collections.Counter).sum()

        items = [[k, frequencies[k]] for k, v in frequencies.items()]
        # items = [[k, frequencies[k], descriptions[k]] for k, v in frequencies.items()]

        # As a data frame
        frame = pd.DataFrame(data=items, columns=['tag', 'frequency'])
        # frame = pd.DataFrame(data=items, columns=['tag', 'frequency', 'group'])
        # frame = frame.copy().merge(self.__tags[['tag', 'annotation_name']], on='tag', how='left')
        frame.rename(columns={'frequency': stem}, inplace=True)
        frame.set_index(keys='tag', drop=True, inplace=True)

        return frame


    def exc(self, architecture: str):

        uri_ = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, architecture, 'data', '*.csv'))

        computations = []
        for uri in uri_:
            data = self.__data(uri=uri)
            frequencies = self.__frequencies(data=data, stem=pathlib.Path(uri).stem)
            logging.info(frequencies)
            computations.append(frequencies)
        frame = pd.concat(computations, axis=1, ignore_index=False)
        frame.reset_index(drop=False, inplace=True)

        data = frame.copy().merge(self.__tags.copy()[['tag', 'annotation_name', 'group']], how='left', on='tag')
        logging.info(data)
        data.info()

        for i in range(data.shape[0]):

            x = data.loc[i, self.__categories].to_json(orient='split')
            y = json.loads(x)
            logging.info(y)



