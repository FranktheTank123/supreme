from __future__ import print_function

from BeautifulSoup import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

try:
	from config.info import *
except:
	print("No info found. Use template.")
	from config.info_template import *

class SupremeItems(object):
	@staticmethod
	def get_all_supreme_items():
		req = requests.get('http://www.supremenewyork.com/shop/all')
		soup = BeautifulSoup(req.text)
		all_href = soup.findAll('a', href=True)

		links = []
		for a in all_href:
			_href = a['href']
			if _href.startswith('/shop') and len(_href.split('/'))==5:
				links.append('http://www.supremenewyork.com' + _href)
		return links


class SupremeShopper(object):
	def __init__(self):
		self._checkout_url = 'https://www.supremenewyork.com/checkout'
		self._home_page = 'http://www.supremenewyork.com/shop/all'

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
		self.supreme_items = SupremeItems()
		self.last_all_supreme_items = []
		self.new_supreme_items = [
			'http://www.supremenewyork.com/shop/pants/zix4b8kaf/hbs9kyrg0',
			'http://www.supremenewyork.com/shop/accessories/jy1cn3sie/eq35gubw7'
		]

	def monitor_new_items(self, sleep=2, max_count=1):
		count = 0
		current_all_supreme_items = self.supreme_items.get_all_supreme_items()
		
		while (len(self.last_all_supreme_items)==0 or len(current_all_supreme_items) == len(self.last_all_supreme_items)) and count<max_count:
			time.sleep(sleep)
			self.last_all_supreme_items = current_all_supreme_items
			current_all_supreme_items = self.supreme_items.get_all_supreme_items()
			count += 1
			print("count: {} out of {}".format(count, max_count))

		self.new_supreme_items = list(set(current_all_supreme_items) - set(self.last_all_supreme_items))
		self.last_all_supreme_items = current_all_supreme_items

	@property
	def checkout(self):
		self.go_to_checkout()
		self.fill_checkout_info
		self.click_process_payment

	@property
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

	@property
	def add_item(self):
		self.driver.find_element_by_name('commit').click() # add to cart
		# try: 
		# 	self.driver.find_element_by_class_name('delete')
		# except:
		# 	return
		# else:
		# 	self.driver.find_element_by_name('commit').click()

	@property
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

	@property
	def click_process_payment(self):
		if self.driver.current_url != self._checkout_url:
			return # TODO: raise error here
		self.driver.find_element_by_name('commit').click()

	@property
	def add_all_new_items(self):
		for i in range(len(self.new_supreme_items)):
			try:
				self.go_to_item(i)
				time.sleep(0.5)
				self.add_item
			except:
				pass

if __name__ == '__main__':
	ss = SupremeShopper()
	ss.go_home_page
	# ss.monitor_new_items()

	ss.add_all_new_items
	time.sleep(0.5)
	ss.checkout