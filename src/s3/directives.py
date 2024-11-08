
import dask

import pandas as pd
import subprocess

import src.elements.s3_parameters as s3p


class Directives:

    def __init__(self, s3_parameters: s3p.S3Parameters):

        self.__s3_parameters = s3_parameters

    @dask.delayed
    def __unload(self, src: str, dst: str):

        path = f's3://{self.__s3_parameters.internal}/{src}/'

        state = subprocess.run(f'aws s3 cp {path} {dst} --recursive', shell=True, check=True)

        return state

    def exc(self, source: pd.Series, destination: pd.Series):


        computation = []
        for src, dst in zip(source, destination):

            self.__unload(src=src, dst=dst)
