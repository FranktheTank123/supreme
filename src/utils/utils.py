from __future__ import print_function, absolute_import

import time

def timeit(method):
    def timed(*args, **kw):
        print('{} start.'.format(method.__name__))
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('{} end, takes  {:.4f}s.'.format(method.__name__, (te - ts)))
        return result
    return timed


if __name__ == '__main__':
    @timeit
    def ji(x,y,z=1):
        return x**y**z

    ji(3,1,2)
