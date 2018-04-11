from __future__ import print_function

import json
import time
import sys


from src.supreme_items_monitor import SupremeItemsMonitor
from src.supreme_shopper import SupremeShopper


def contains(name, name_list):
    return any([True if x in name.lower() else False for x in name_list])

def filter_names(new_inventory, name_list):
    return {k: v for k, v in new_inventory.iteritems() if contains(v, name_list)}

if __name__ == '__main__':
    # load data
    datestr = '2018-04-11'
    with open('data/supreme_list_{}.json'.format(datestr), 'r') as f:
        inventory = json.load(f)

    # test or not
    if len(sys.argv)>1 and sys.argv[1] == 'test':
        sleep_time = 100
        name_list = ['nylon turnout jacket', 'tagless tees']  # test
        del inventory['https://www.supremenewyork.com/shop/accessories/b82ba9vpq/jx7qm1hsc']
        # inventory = {}
    else:
        sleep_time = 1000
        name_list = ['cactus keychain', 'rimowa']

    # get refreshed items every 0.5 secs
    si = SupremeItemsMonitor(inventory)
    new_inventory = si.monitor(sleep=0.5, max_count=-1)
    print("Found {} new items.".format(len(new_inventory)))

    # filter what we want
    new_inventory = filter_names(new_inventory, name_list)
    print("After filtering, we have {} new item, they are:".format(len(new_inventory)))
    for _, name in new_inventory.iteritems():
        print(name)

    # place order
    lst = new_inventory.keys()
    ss = SupremeShopper()
    ss.shop(lst)

    time.sleep(sleep_time)
