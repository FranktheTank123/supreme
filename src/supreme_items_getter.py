from __future__ import print_function, absolute_import

from BeautifulSoup import BeautifulSoup
import multiprocessing as mp
import re
import requests

from src.utils.logger import get_logger
from src.utils.utils import timeit

logger = get_logger()

SUPREME_HOME = 'https://www.supremenewyork.com'
SUPREME_SHOP_ALL = '/shop/all'
HEADERs = {"content-type": "text"}  # request headers

def item_name_getter(link):
    req = requests.get(link,  headers=HEADERs)
    item_name = re.findall('<title>(.*?)</title>', req.text)[0]  # this is faster than below
    # soup = BeautifulSoup(req.text)
    # item_name = soup.find('title').text
    return {link: item_name}

class SupremeItemsGetter(object):
    @staticmethod
    def get_all_supreme_links():
        """
         Send request to SUPREME_HOME and return all shopping items

        :return:
        """
        req = requests.get(SUPREME_HOME + SUPREME_SHOP_ALL,  headers=HEADERs)
        soup = BeautifulSoup(req.text)
        all_href = soup.findAll('a', href=True)
        links = []
        for a in all_href:
            _href = a['href']
            if _href.startswith('/shop') and len(_href.split('/') ) == 5:
                # we want _href look like: /shop/pants/zix4b8kaf/hbs9kyrg0
                links.append(SUPREME_HOME + _href)
        logger.info('Found {} linkes from shop/all'.format(len(links)))
        return links

    @staticmethod
    def filter_by_category(links, category):
        """
        If we specify category, we will only look into these links

        :param links: list of full urls, e.g.: 'http://www.supremenewyork.com/shop/bags/ohdvjknl0/rq701cpgw'
        :return: filtered links
        """
        if category is None:
            return links
        else:
            return [x for x in links if x.split('/')[4] in category]

    @staticmethod
    def create_inventory(links, parallel=True):
        if parallel:
            return SupremeItemsGetter._create_inventory_fast(links)

        pool_outputs = [item_name_getter(link) for link in links]
        return {k: v for d in pool_outputs for k, v in d.iteritems()}

    @staticmethod
    def _create_inventory_fast(links):
        """
        Parallel version of create_inventory
        """
        n_processes = mp.cpu_count()
        pool = mp.Pool(processes=n_processes*3) # over-threading if needed
        pool_outputs = pool.map(item_name_getter, links)
        pool.close()
        pool.join()
        return {k: v for d in pool_outputs for k, v in d.iteritems()}


if __name__ == '__main__':
    si = SupremeItemsGetter()
    links = si.get_all_supreme_links()
    links = si.filter_by_category(links, ['bags'])
    inventory = si.create_inventory(links, parallel=False)
    inventory = si.create_inventory(links, parallel=True)