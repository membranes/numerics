"""Module latest.py"""
import datetime
import logging
import os
import sys
import time
import glob

import config
import src.functions.objects


class Latest:
    
    def __init__(self):
        """
        Constructor
        """
        
        self.__configurations = config.Config()
        
        # The path to the latest best model ...
        self.__latest_ = os.path.join(self.__configurations.numerics_, 'best')

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __get_time(pathstr: str) -> str:
        """

        :param pathstr:
        :return:
        """

        seconds: float = os.path.getmtime(pathstr)
        stamp: str = time.ctime(seconds)
        structure: time.struct_time = time.strptime(stamp)
        text: str = time.strftime('%Y-%m-%d %H:%M:%S', structure)

        return text
    
    def exc(self):
        """
        
        :return: 
        """

        listing = glob.glob(pathname=os.path.join(self.__latest_, 'model', '*.safetensors'))

        # Asset time stamp; determining a file's modification or creation/re-creation date & time stamp
        if len(listing) == 1:
    
            text = self.__get_time(pathstr=listing[0])
    
            nodes = {"time": text}
            message = src.functions.objects.Objects().write(
                nodes=nodes, path=os.path.join(self.__latest_, 'latest.json'))
            self.__logger.info(message)
            
        else:
            
            raise f'A *.safetensors model file was not found in {self.__latest_}{os.sep}model{os.sep}'
    
    