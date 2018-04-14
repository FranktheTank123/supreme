from __future__ import print_function, absolute_import

import json
import time
from selenium import webdriver

from src.utils.utils import timeit

class SupremeShopper(object):
    def __init__(self, config_loader, autofill_on=True, keywords=[], size=[]):
        # constants
        self._checkout_url = 'https://www.supremenewyork.com/checkout'
        self._home_page = 'https://www.supremenewyork.com/shop/all'
        self._recaptcha_url = 'https://checkmeout.pro/recaptcha'

        # set-up specific
        self.config_loader = config_loader  # payment info
        self.autofill_on = autofill_on

        # filter specific
        self.keywords = keywords  # ['rimowa', 'red']  # use when filter
        self.size = size #  ['Small', 'Medium', 'Large', 'XLarge']  # use when shopping

        self.candidate_items = {}
        self.max_items_in_cart = 1 # right now we only shop 1 items per order
        self.current_items_in_cart = 0
        self.items_in_cart = []

    def set_up_driver(self):
        if self.autofill_on:
            autofill_activator = AutofillActivator()
            chrome_options = autofill_activator.get_options
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            autofill_activator.set_driver(ss.driver)
            autofill_activator.dump_info(cl.info)
        else:
            self.driver = webdriver.Chrome(chrome_options=None)
        self.driver.get(self._home_page)

    def set_up_recaptcha(self):
        """
        Go to trigger recaptcha.
        """

        self.driver.execute_script("window.open('{}');".format(self._recaptcha_url))
        self.driver.switch_to.window(self.driver.window_handles[1])
        for i in range(5):
            try:
                self.driver.find_element_by_css_selector('button.g-recaptcha.button.special.big').click()
                time.sleep(0.1)
            except:
                pass
        self.driver.switch_to.window(self.driver.window_handles[0])

    def wait_then_process(self):
        new_items = self._wait_for_list()
        self.candidate_items = self.filter_names(new_items, self.keywords)

    @staticmethod
    def _wait_for_list():
        refresh_time = 1
        while True:
            time.sleep(refresh_time)
            try:
                with open('data/_new_inventory.json', 'r') as f:
                    new_inventory = json.load(f)
                    return new_inventory
            except:
                print('Load new inventory failed, try again in {} seconds.'.format(refresh_time))

    @staticmethod
    def filter_names(new_inventory, keywords):
        def contains(name, keywords):
            return all([y.lower() in name for y in keywords])
        return {k: v for k, v in new_inventory.iteritems() if contains(v.lower(), keywords)}

    @timeit
    def shop(self):
        self.add_items()
        time.sleep(0.3)
        self.checkout()

    def add_items(self):
        for url, name in self.candidate_items.iteritems():
            if not self._ready_to_checkout:
                try:
                    self._add_item(url)
                    self.current_items_in_cart += 1
                    print('Added: {}'.format(name))
                except:
                    pass
        return

    def _add_item(self, url):
        self.driver.get(url)
        time.sleep(0.3)
        self._specify_size()
        self._add_to_cart()

    def _specify_size(self):
        for _size in self.size:
            try:
                self._select_size(_size)
                break
            except:
                pass
        return

    def _select_size(self, size):
        self.driver.find_element_by_xpath(".//select[@name='s']").send_keys('Large')

    def _add_to_cart(self):
        self.driver.find_element_by_xpath(".//input[@value='add to cart']").click()

    @property
    def _ready_to_checkout(self):
        return self.current_items_in_cart >= self.max_items_in_cart

    @timeit  # benchmark: with autofill: 2s, without autofill: 8s
    def checkout(self):
        self.driver.get(self._checkout_url)  # this takes ~1s
        if not self.autofill_on:
            self._fill_checkout_info()
        self._click_agree_terms()
        self._click_process_payment()

    def _fill_checkout_info(self):
        self.driver.find_element_by_xpath(".//input[@name='order[billing_name]']").send_keys(self.config_loader.info['billing_name'])
        self.driver.find_element_by_xpath(".//input[@name='order[email]']").send_keys(self.config_loader.info['email'])
        self.driver.find_element_by_xpath(".//input[@name='order[tel]']").send_keys(self.config_loader.info['tel'])
        self.driver.find_element_by_xpath(".//input[@name='order[billing_address]']").send_keys(self.config_loader.info['billing_address'])
        self.driver.find_element_by_xpath(".//input[@name='order[billing_address_2]']").send_keys(self.config_loader.info['billing_address_2'])
        self.driver.find_element_by_xpath(".//input[@name='order[billing_zip]']").send_keys(self.config_loader.info['billing_zip'])

        self.driver.find_element_by_xpath(".//input[@name='credit_card[nlb]']").send_keys(self.config_loader.info['nlb'])
        self.driver.find_element_by_xpath(".//select[@name='credit_card[month]']").send_keys(self.config_loader.info['month'])
        self.driver.find_element_by_xpath(".//select[@name='credit_card[year]']").send_keys(self.config_loader.info['year'])
        self.driver.find_element_by_xpath(".//input[@name='credit_card[rvv]']").send_keys(self.config_loader.info['rvv'])

    def _click_agree_terms(self):
        self.driver.find_element_by_xpath(".//*[contains(text(), 'I have read and agree')]").click()

    def _click_process_payment(self):
        self.driver.find_element_by_name('commit').click()



if __name__ == '__main__':
    from src.autofill_activator import AutofillActivator
    from src.config_loader import ConfigLoader

    # warm up the environment
    cl = ConfigLoader(test=True)
    ss = SupremeShopper(cl, autofill_on=True)
    ss.set_up_driver()
    # ss.set_up_recaptcha()

    ss.wait_then_process()
    # ss.candidate_items = {
    #     'http://www.supremenewyork.com/shop/jackets/swrpxs4j6/wuz75j1ev':
    #         'Supreme: World Famous Taped Seam Hooded Pullover - Acid Green',
    #     'http://www.supremenewyork.com/shop/jackets/swrpxs4j6/hq5dz10gv':
    #         'Supreme: World Famous Taped Seam Hooded Pullover - Red'
    # }
    ss.shop()