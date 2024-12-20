
import logging

import pandas as pd

import src.elements.text_attributes as txa
import src.functions.streams

import src.elements.s3_parameters as s3p


class Tags:
    """
    Tags
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

    def exc(self) -> pd.DataFrame:

        # The <tags> inventory
        uri = 's3://' + self.__s3_parameters.configurations + '/labels/tags.csv'
        text = txa.TextAttributes(uri=uri, header=0)
        streams = src.functions.streams.Streams()
        tags = streams.read(text=text)
        logging.info(tags)

        return tags
