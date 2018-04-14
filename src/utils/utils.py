from __future__ import print_function, absolute_import

import time

from src.utils.logger import get_logger

logger = get_logger()

def timeit(method):
    def timed(*args, **kw):
        logger.info('{} start.'.format(method.__name__))
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info('{} end, takes  {:.4f}s.'.format(method.__name__, (te - ts)))
        return result
    return timed


if __name__ == '__main__':
    @timeit
    def ji(x,y,z=1):
        return x**y**z

    ji(3,1,2)
