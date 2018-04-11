try:
    from config.info import infos
except:
    print("No info found. Use template.")
    from config.info_template import infos

import random

class ConfigLoader(object):
    def __init__(self, i=-1):
        try:
            self.info = infos[i]
        except:
            self.info = random.choice(infos)

    @property
    def order_dict(self):
        keys = [
            'billing_name', 'email', 'tel', 'billing_address', 'billing_address_2',
            'billing_zip',
            # 'billing_city', 'billing_state', 'billing_country'
        ]
        return [(k, self.info[k]) for k in keys]

    @property
    def cc_dict(self):
        keys = ['nlb', 'month', 'year', 'rvv']
        return [(k, self.info[k]) for k in keys]
