from __future__ import print_function

import json
import time
from tqdm import tqdm
import random
import sys

from src.config_loader import ConfigLoader
from src.supreme_items_monitor import SupremeItemsMonitor
from src.supreme_shopper import SupremeShopper


def contains(name, name_list):
    return any([all([y.lower() in name for y in x]) for x in name_list])
    # return any([True if x in name.lower() else False for x in name_list])

def filter_names(new_inventory, name_list):
    return {k: v for k, v in new_inventory.iteritems() if contains(v.lower(), name_list)}

def sleep(sec):
    sec = int(sec)
    for _ in tqdm(range(sec), desc='Sleep for {} seconds:'.format(sec)):
        time.sleep(1)


if __name__ == '__main__':
    # load data
    MAX_ITEM = 2
    datestr = '2018-04-11'
    with open('data/supreme_list_{}.json'.format(datestr), 'r') as f:
        inventory = json.load(f)

    # test or not
    if len(sys.argv)>1 and sys.argv[1] == 'test':
        from config.info_template import infos
        sleep_time = 10
        name_list = [['nylon','turnout', 'jacket', 'olive'], ['tagless, tees']]  # test
        inventory = {}
    else:
        from config.info import infos
        sleep_time = 1000
        name_list = [['cactus', 'keychain'], ['rimowa', 'red']]


    # get refreshed items every 0.5 secs
    config_loader = ConfigLoader(infos)
    ss = SupremeShopper(config_loader)
    ss.recaptcha()
    si = SupremeItemsMonitor(inventory)
    new_inventory = si.monitor(sleep=0.5, max_count=-1)
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        sleep(5)
    print("Found {} new items.".format(len(new_inventory)))

    # filter what we want
    new_inventory = filter_names(new_inventory, name_list)
    print("After filtering, we have {} new item, they are:".format(len(new_inventory)))
    for _, name in new_inventory.iteritems():
        print(name.encode("utf-8"))

    # place order
    lst = random.sample(new_inventory.keys(), min(MAX_ITEM, len(new_inventory.keys())))
    print("Randomly select {} items:".format(MAX_ITEM))
    for l in lst:
        print(new_inventory[l].encode("utf-8"), ":", l)

    ss.shop(lst)

    sleep(sleep_time)
