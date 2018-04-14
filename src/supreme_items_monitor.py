from __future__ import print_function, absolute_import

import json

from src.utils.utils import timeit
from src.supreme_items_getter import SupremeItemsGetter


class SupremeItemsMonitor(object):
    def __init__(self, category=None):
        self.black_list = []
        self.category = category
        self.items_getter = SupremeItemsGetter()

    def gen_black_list(self):
        """
        This will be run before the drop. Ideally everything will be not interested

        :return:
        """
        self.black_list = self.items_getter.get_all_supreme_links()

    @timeit # benchmark 0.5s
    def monitor(self):
        while True:
            links = self.items_getter.get_all_supreme_links()
            links = set(links) - set(self.black_list)  # updated links by taking the differences
            if len(links):
                links = self.items_getter.filter_by_category(links, self.category)
                new_inventory = self.items_getter.create_inventory(links, parallel=True)
                with open('data/_new_inventory.json', 'w') as f:
                    json.dump(new_inventory, f)
                return new_inventory

if __name__ == '__main__':
    sm = SupremeItemsMonitor(category=['bags'])
    # sm.gen_black_list()
    new_inventory = sm.monitor()