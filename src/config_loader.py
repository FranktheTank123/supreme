from __future__ import print_function, absolute_import

import os
import random
import yaml

class ConfigLoader(object):
    def __init__(self, test=False):
        if test or not os.path.isfile('config/info.yaml'):
            with open('config/info_template.yaml', 'r') as f:
                infos = yaml.load(f)

        else:
            with open('config/info.yaml', 'r') as f:
                infos = yaml.load(f)

        accout = random.choice(infos.keys())
        self._info = infos[accout]

    @property
    def info(self):
        return self._info

    @property
    def order_info(self):
        keys = [
            'billing_name', 'email', 'tel', 'billing_address', 'billing_address_2',
            'billing_zip',
            'billing_city', 'billing_state', 'billing_country'
        ]
        return [(k, self.info[k]) for k in keys]

    @property
    def cc_info(self):
        keys = ['nlb', 'month', 'year', 'rvv']
        return [(k, self.info[k]) for k in keys]


if __name__ == '__main__':
    cl = ConfigLoader()
    order_info = cl.order_info
    cc_info = cl.cc_info