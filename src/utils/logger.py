from __future__ import print_function, absolute_import

import coloredlogs
import datetime
import logging
import os

def get_logger():
    initialize_logger()
    logger = logging.getLogger('supreme')
    return logger


def initialize_logger(count=[]):
    if len(count) == 0:  # singleton
        log_dir = 'logs'
        time =  datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        logger = logging.getLogger('supreme')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # create the logging file handler
        coloredlogs.install(fmt='%(asctime)s - %(levelname)s - %(message)s', logger=logger)
        coloredlogs.install(fmt='%(asctime)s - %(levelname)s - %(message)s', logger=logger,
                            stream=open(os.path.join(log_dir, '{}.log'.format(time)), 'w'))

        count.append(1)
    else:
        return