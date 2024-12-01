"""Module hyperspace.py"""
import json

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.unload


class Limits:
    """
    Class Limits
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 (Simple Storage Service) parameters
                              settings of this project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters = s3_parameters

        # Prefix: The segments between the bucket name and a target file name.
        self.__prefix = 'limits/'

    def __get_dictionary(self, key_name: str) -> dict:
        """
        s3:// {bucket.name} / {prefix} & {filename}

        :param key_name: {prefix} & {filename}
        :return:
        """

        buffer = src.s3.unload.Unload(s3_client=self.__service.s3_client).exc(
            bucket_name=self.__s3_parameters.configurations, key_name=key_name)
        dictionary = json.loads(buffer)

        return dictionary

    def exc(self, filename: str) -> dict:
        """
        s3:// {bucket.name} / {prefix} & {filename}

        :param filename: A file's name, including its extension.
        :return:
        """

        # Get the dictionary of ...
        dictionary = self.__get_dictionary(key_name=f'{self.__prefix}{filename}')

        return dictionary
