"""Module directives.py"""
import os
import subprocess
import sys

import dask
import pandas as pd

import src.elements.s3_parameters as s3p
import src.functions.directories


class Directives:
    """
    Class Directives
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

        # Directories instances
        self.__directories = src.functions.directories.Directories()

    @dask.delayed
    def __unload(self, origin: str, target: str) -> int:
        """

        :param origin:
        :param target:
        :return:
        """

        # Create the destination directory
        self.__directories.create(path=target)

        # Hence
        destination = target.replace(os.getcwd() + os.path.sep, '')
        source = f"s3://{self.__s3_parameters.internal}/{origin}/"
        state = subprocess.run(f"aws s3 cp {source} {destination}/ --recursive", shell=True, check=True)

        return state.returncode

    def exc(self, source: pd.Series, destination: pd.Series):
        """

        :param source:
        :param destination:
        :return:
        """

        computation = []
        for origin, target in zip(source, destination):
            state = self.__unload(origin=origin, target=target)
            computation.append(state)
        executions: list[int] = dask.compute(computation, scheduler='threads')[0]

        if all(executions) == 0:
            return True

        sys.exit('Artefacts download step failure.')
