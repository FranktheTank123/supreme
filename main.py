from __future__ import print_function

import json

from src.supreme_items_monitor import SupremeItemsMonitor
from src.supreme_shopper import SupremeShopper


def contains(name, name_list):
    return any([True if x in name.lower() else False for x in name_list])

def filter_names(new_inventory, name_list):
    return {k: v for k, v in new_inventory.iteritems() if contains(v, name_list)}

if __name__ == '__main__':
    datestr = '2018-04-11'
    # name_list = ['cactus keychain', 'rimowa']
    name_list = ['nylon turnout jacket', 'world famous rayon shirt'] # test

    with open('data/supreme_list_{}.json'.format(datestr), 'r') as f:
        inventory = json.load(f)

    # test
    # del inventory['https://www.supremenewyork.com/shop/accessories/b82ba9vpq/jx7qm1hsc']
    inventory = {}


    si = SupremeItemsMonitor(inventory)
    new_inventory = si.monitor(sleep=0.5, max_count=-1)
    print("Found {} new items.".format(len(new_inventory)))

    new_inventory = filter_names(new_inventory, name_list)
    print("After filtering, we have {} new item, they are:".format(len(new_inventory)))
    for _, name in new_inventory.iteritems():
        print(name)

    lst = new_inventory.keys()
    ss = SupremeShopper()
    ss.shop(lst)