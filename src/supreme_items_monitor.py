from __future__ import print_function, absolute_import

import json
import time

from src.supreme_items_getter import SupremeItemsGetter
from src.utils.logger import get_logger
# from src.utils.utils import timeit

logger = get_logger()

class SupremeItemsMonitor(object):
    def __init__(self, category=None, refresh_time=1):
        self.black_list = []
        self.category = category
        self.items_getter = SupremeItemsGetter()
        self.refresh_time = refresh_time

    def gen_black_list(self):
        """
        This will be run before the drop. Ideally everything will be not interested

        :return:
        """
        self.black_list = self.items_getter.get_all_supreme_links()
        logger.info('Blacklist generated, which contains {} items.'.format(len(self.black_list)))

    # @timeit # benchmark 0.5s
    def monitor(self):
        while True:
            links = self.items_getter.get_all_supreme_links()
            links = set(links) - set(self.black_list)  # updated links by taking the differences
            if len(links):
                logger.info('Found {} new items. Start category filter.'.format(len(links)))
                links = self.items_getter.filter_by_category(links, self.category)
                new_inventory = self.items_getter.create_inventory(links, parallel=True)
                logger.info('Filtering done. Write {} items into disk to shop.'.format(len(new_inventory)))
                with open('data/_new_inventory.json', 'w') as f:
                    json.dump(new_inventory, f)
                return new_inventory
            else:
                logger.warn('No new items found from shop/all. Will do it again in {} sec.'.format(self.refresh_time))
                time.sleep(self.refresh_time)

if __name__ == '__main__':
    sm = SupremeItemsMonitor(category=['jackets'])
    # sm.gen_black_list()
    new_inventory = sm.monitor()