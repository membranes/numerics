import logging
import os

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.prefix


class Architectures:
    """
    The artefacts per architecture
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service = service
        self.__s3_parameters = s3_parameters

        self.__configurations = config.Config()
        self.__prefix = self.__s3_parameters.path_internal_artefacts

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __keys(self) -> list:
        """

        :return:
        """

        listings: list = src.s3.prefix.Prefix(
            service=self.__service, bucket_name=self.__s3_parameters.internal).objects(prefix=self.__prefix)

        return listings

    def __excerpt(self, keys: list) -> list:
        """
        Extracts the keys within prime/model directory

        :param keys:
        :return:
        """

        listings: list = [k for k in keys if k.__contains__(self.__configurations.prime_model_anchor)]

        return listings

    def __strings(self, keys: list[str]) -> pd.DataFrame:
        """

        :param keys: A list of Amazon S3 keys, i.e., prefix + vertex
        :return:
        """

        # A data frame consisting of the S3 keys, the vertex of each
        # key, i.e., file name + extension
        frame = pd.DataFrame(data={'key': keys})
        frame = frame.assign(vertex=frame['key'].str.rsplit('/', n=1, expand=True)[1])

        # And, the local storage string of each file ...
        # Reducing the hierarchy of directories
        frame = frame.assign(filename=frame['key'])
        frame['filename'] = frame['filename'].replace(to_replace=self.__configurations.prime_model_anchor, value='', regex=True)

        # Ascertaining that the appropriate directory separator is in place
        # Hence, the storage strings
        frame = frame.assign(filename=frame['filename'].replace(to_replace='/', value=os.path.sep))
        frame = frame.assign(filename=self.__configurations.data_ + os.path.sep + frame['filename'])

        return frame

    def __paths(self, keys: list[str]):

        # A data frame consisting of the S3 keys
        frame = pd.DataFrame(data={'key': keys})
        frame = frame.assign(key=frame['key'].str.rsplit('/', n=1, expand=True)[0])
        frame.drop_duplicates(inplace=True)

        # And corresponding local counterparts
        frame['path'] = frame['key'].copy().replace(to_replace=self.__configurations.prime_model_anchor, value='', regex=True)
        frame = frame.assign(path=frame['path'].replace(to_replace='/', value=os.path.sep))
        frame['path'] = self.__configurations.data_ + os.path.sep + frame['path']

        print(frame)

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # Determining the unique list of fine-tuned models
        keys = self.__keys()
        keys = self.__excerpt(keys=keys)

        self.__paths(keys=keys)

        strings = self.__strings(keys=keys)

        return strings
