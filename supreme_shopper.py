from __future__ import print_function

try:
    from config.info import *
except:
    print("No info found. Use template.")
    from config.info_template import *

from selenium import webdriver
import time
import sys


class SupremeShopper(object):
    def __init__(self):
        self._checkout_url = 'https://www.supremenewyork.com/checkout'
        self._home_page = 'http://www.supremenewyork.com/shop/all'
        self.new_supreme_items = []
        self.driver = webdriver.Chrome()

        self.order_dict = {
            'billing_name': BILLING_NAME,
            'email': EMAIL,
            'tel': TEL,
            'billing_address': BILLING_ADDRESS,
            'billing_address_2': BILLING_ADDRESS_2,
            'billing_zip': BILLING_ZIP,
            # 'billing_city': BILLING_CITY,
        }
        self.cc_dict = {
            'nlb': (NLB, True),
            'month': (MONTH, False),
            'year': (YEAR, False),
            'rvv': (RVV, True)
        }

    def shop(self, lst):
        self.set_new_supreme_items(lst)
        self.add_all_new_items()
        self.checkout()


    def set_new_supreme_items(self, new_supreme_items):
        self.new_supreme_items = new_supreme_items

    def checkout(self):
        self.go_to_checkout()
        self.fill_checkout_info()
        self.click_process_payment()

    def go_home_page(self):
        self.driver.get(self._home_page)

    def go_to_checkout(self, n=5, sleep=0.5):
        """
        Go to checkout page, try n times. Will fail if nothing has been add to cart
        """
        self.driver.get(self._checkout_url)
        if self.driver.current_url != self._checkout_url:
            print("Go to checkout failed. Try {} more times in {} seconds".format(n, sleep))
            time.sleep(sleep)
            self.go_to_checkout(n=n-1)

    def go_to_item(self, i=0):
        self.driver.get(self.new_supreme_items[i])

    def add_item(self):
        self.driver.find_element_by_name('commit').click() # add to cart
        # try:
        #     self.driver.find_element_by_class_name('delete')
        # except:
        #     return
        # else:
        #     self.driver.find_element_by_name('commit').click()

    def fill_checkout_info(self):
        if self.driver.current_url != self._checkout_url:
            return # TODO: raise error here

        # fillout
        for key, value in self.order_dict.iteritems():
            elem = self.driver.find_element_by_name('order[{}]'.format(key))
            elem.clear()
            elem.send_keys(value)

        for key, (value, clear) in self.cc_dict.iteritems():
            elem = self.driver.find_element_by_name('credit_card[{}]'.format(key))
            if clear:
                elem.clear()
            elem.send_keys(value)

        self.driver.find_element_by_xpath(".//*[contains(text(), 'I have read and agree')]").click()

        # assert self.driver.find_element_by_name('order[billing_city]').get_attribute('value') == BILLING_CITY
        # assert self.driver.find_element_by_name('order[billing_state]').get_attribute('value') == BILLING_STATE
        # assert self.driver.find_element_by_name('order[billing_country]').get_attribute('value') == BILLING_COUNTRY

    def click_process_payment(self):
        if self.driver.current_url != self._checkout_url:
            return # TODO: raise error here
        self.driver.find_element_by_name('commit').click()

    def add_all_new_items(self):
        for i in range(len(self.new_supreme_items)):
            try:
                self.go_to_item(i)
                time.sleep(0.5)
                self.add_item()
                time.sleep(0.5)
            except:
                pass

if __name__ == '__main__':
    if sys.argv[1] is not None:
        lst = [sys.argv[1]]
    else:
        lst = [
            'https://www.supremenewyork.com/shop/pants/zix4b8kaf/hbs9kyrg0',
            'https://www.supremenewyork.com/shop/accessories/jy1cn3sie/eq35gubw7'
        ]
    ss = SupremeShopper()
    ss.shop(lst)
    # ss.set_new_supreme_items(lst)
    # ss.add_all_new_items()
    # ss.checkout()

    