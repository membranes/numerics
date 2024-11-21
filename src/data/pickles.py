import glob
import logging
import os
import pickle

import config


class Pickles:

    def __init__(self):

        self.__configurations = config.Config()

    def exc(self):

        listings = glob.glob(pathname=os.path.join(self.__configurations.artefacts_, '**', '*.pkl'), recursive=True)

        logging.info(listings)

        for listing in listings:

            logging.info('Extracting %s ...', listing)

            with open(file=listing, mode='rb') as disk:
                content = pickle.load(disk)

            logging.info(content)
