import os
import dask
import sys

import pandas as pd
import subprocess

import src.elements.s3_parameters as s3p
import src.functions.directories


class Directives:

    def __init__(self, s3_parameters: s3p.S3Parameters):

        self.__s3_parameters = s3_parameters

        self.__directories = src.functions.directories.Directories()

    @dask.delayed
    def __unload(self, src: str, dst: str) -> int:

        self.__directories.create(path=dst)
        target = dst.replace(os.getcwd() + os.path.sep, '')

        path = f"s3://{self.__s3_parameters.internal}/{src}/"
        state = subprocess.run(f"aws s3 cp {path} {target}/ --recursive", shell=True, check=True)

        return state.returncode

    def exc(self, source: pd.Series, destination: pd.Series):


        computation = []
        for src, dst in zip(source, destination):
            state = self.__unload(src=src, dst=dst)
            computation.append(state)

        executions: list[int] = dask.compute(computation, scheduler='threads')[0]

        if all(executions) == 0:
            return True

        sys.exit('Artefacts download failures.')
