from __future__ import print_function

from BeautifulSoup import BeautifulSoup
import multiprocessing as mp
import requests
import time
from tqdm import tqdm
import json

SUPREME_HOME = 'https://www.supremenewyork.com'
SUPREME_SHOP_ALL = '/shop/all'


def item_name_getter(link):
    req = requests.get(link,  headers={"content-type":"text"})
    soup = BeautifulSoup(req.text)
    item_name = soup.find('title').text
    return {link: item_name}

class SupremeItemsMonitor(object):
    def __init__(self, inventory):
        self.inventory = inventory     # href => name

    @staticmethod
    def get_all_supreme_links():
        req = requests.get(SUPREME_HOME + SUPREME_SHOP_ALL,  headers={"content-type":"text"})
        soup = BeautifulSoup(req.text)
        all_href = soup.findAll('a', href=True)
        links = []
        for a in all_href:
            _href = a['href']
            if _href.startswith('/shop') and len(_href.split('/') ) ==5:
                # we want _href look like: /shop/pants/zix4b8kaf/hbs9kyrg0
                links.append(SUPREME_HOME + _href)
        return links

    def create_new_inventory(self, links, parallel=True):
        if parallel:
            return self._create_new_inventory_fast(links)

        new_inventory = {}
        for link in tqdm(links, total=len(links), desc='Inventory'):
            req = requests.get(link,  headers={"content-type":"text"})
            soup = BeautifulSoup(req.text)
            item_name = soup.find('title').text
            new_inventory[link] = item_name
        return new_inventory

    def _create_new_inventory_fast(self, links):
        """
        Parallel version of create_new_inventory
        """
        n_processes = mp.cpu_count()
        pool = mp.Pool(processes=n_processes*3) # over-threading
        pool_outputs = pool.map(item_name_getter, links)
        pool.close()
        pool.join()
        return {k: v for d in pool_outputs for k, v in d.iteritems()}

    @property
    def get_inventory_links(self):
        return self.inventory.keys()

    def update_inventory(self, new_inventory):
        self.inventory.update(new_inventory)

    def monitor(self, sleep=1, max_count=5):
        """

        :param sleep:
        :param max_count: when < 0, will run until new tiems come
        :return:
        """
        count = 0
        current_links = self.get_all_supreme_links()

        while set(current_links) == set(self.get_inventory_links):
            if max_count >= 0 and count >= max_count:
                break
            time.sleep(sleep)
            current_links = self.get_all_supreme_links()
            count += 1
            print("count: {} out of {}".format(count, max_count))

        new_links = set(current_links) - set(self.get_inventory_links)
        new_inventory = self.create_new_inventory(new_links)
        return new_inventory



if __name__ == '__main__':
    with open('data/supreme_list_2018-04-11.json', 'r') as f:
        inventory = json.load(f)

    si = SupremeItemsMonitor(inventory)
    # new_inventory = si.monitor()
    # with open('data/data.json', 'w') as f:
    #     json.dump(new_inventory, f)
