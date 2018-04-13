from __future__ import print_function, absolute_import

import yaml
import time
from selenium.webdriver.chrome.options import Options

from src.utils.utils import timeit

MAPPING_FILE = 'config/checkout_mapping.yaml'

class AutofillActivator(object):
    def __init__(self):
        self.extension_path = 'chrome/Autofill_v7.8.0.crx'
        self.extension_url = 'chrome-extension://nlmmgnhgdeffjkdckmikfpnddkbbfkkk/options.html'
        self.driver = None

        with open(MAPPING_FILE, 'r') as f:
            self.mapping = yaml.load(f)

    @property
    def get_options(self):
        self.chrome_options = Options()
        self.chrome_options.add_extension(self.extension_path)
        return self.chrome_options

    def set_driver(self, driver):
        self.driver = driver

    @timeit # benchmark 9.5s
    def dump_info(self, info):
        if self.driver is None:
            print('No driver found.')
            return

        self.driver.get(self.extension_url)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="button-close"]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="nav-other"]').click()  # other stuff
        time.sleep(0.5)
        csv = self.get_inport_cvs(info)
        self.driver.find_element_by_xpath('//*[@id="content-ie"]').send_keys(csv)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="button-import"]').click()
        time.sleep(0.5)
        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="nav-fields"]').click()
                break
            except:
                continue
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="button-save"]').click()

    def get_inport_cvs(self, info):
        template = """### PROFILES ###,,,,
Profile ID,Name,Site,Overwrite,
c1,supreme,,1,
### AUTOFILL RULES ###,,,,
Type,Name,Value,Site,Profile
0,"^order\[billing_name\]$","{billing_name}","supremenewyork.com",c1
0,"^order\[email\]$","{email}","supremenewyork.com",c1
0,"^order\[billing_address\]$","{billing_address}","supremenewyork.com",c1
0,"^order\[billing_address_2\]$","{billing_address_2}","supremenewyork.com",c1
0,"^order\[billing_zip\]$","{billing_zip}","supremenewyork.com",c1
0,"^order\[billing_city\]$","{billing_city}","supremenewyork.com",c1
2,"^order\[billing_state\]$","{billing_state}","supremenewyork.com",c1
0,"^order\[tel\]$","{tel}","supremenewyork.com",c1
2,"^credit_card\[year\]$","{year}","supremenewyork.com",c1
2,"^credit_card\[month\]$","{month}","supremenewyork.com",c1
0,"^credit_card\[rvv\]$","{rvv}","supremenewyork.com",c1
0,"^credit_card\[nlb\]$","{nlb}","supremenewyork.com",c1
3,"^order\[terms\]$","1","supremenewyork.com",c1
### OPTIONS ###,,,,
exceptions,"[]",,,
backup,0,100,,
manual,0,,,
delay,0,1,,
labelmatch,1,,,
overwrite,1,,,
vars,1,,,
sound,0,,,
voice,0,1,,
debug,0,,,
mask,1,,,
scale,1,,,
menu,1,,,"""

        res = template.format(
            billing_name=info['billing_name'],
            email=info['email'],
            billing_address=info['billing_address'],
            billing_address_2=info['billing_address_2'],
            billing_zip=info['billing_zip'],
            billing_city=info['billing_city'],
            billing_state=self.mapping['state'][info['billing_state']],
            tel=info['tel'],
            year= self.mapping['cc_year'][info['year']],
            month=self.mapping['cc_month'][info['month']],
            rvv=info['rvv'],
            nlb=info['nlb']
        )
        return res


if __name__ == '__main__':
    from selenium import webdriver

    from src.config_loader import ConfigLoader
    cl = ConfigLoader(test=True)


    aa = AutofillActivator()

    chrome_options = aa.get_options
    driver = webdriver.Chrome(chrome_options=chrome_options)
    aa.set_driver(driver)
    aa.dump_info(cl.info)

    driver.get('http://www.supremenewyork.com/shop/all')
