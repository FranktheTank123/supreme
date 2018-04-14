from __future__ import print_function

import argparse
import time
import yaml

from src.config_loader import ConfigLoader
from src.supreme_items_monitor import SupremeItemsMonitor
from src.supreme_shopper import SupremeShopper


from src.utils.logger import get_logger

logger = get_logger()


def run_both_jobs(args):
    logger.info('One job, easy.')
    config_loader = ConfigLoader(test=args['test'])
    ss = SupremeShopper(config_loader,
                        autofill_on=args['autofill_on'],
                        keywords=args['keywords'],
                        size=args['size'],
                        refresh_time=args['refresh_time'],
                        recaptcha=args['recaptcha'])

    sm = SupremeItemsMonitor(category=args['category'],
                             refresh_time=args['refresh_time'])
    if not args['test']:
        sm.gen_black_list()

    new_inventory = sm.monitor()
    ss.set_up_driver()
    ss.candidate_items = new_inventory
    ss.shop()

def run_monitor(args):
    logger.warn('Monitor only mode.')
    sm = SupremeItemsMonitor(category=args['category'],
                             refresh_time=args['refresh_time'])
    if not args['test']:
        sm.gen_black_list()
    _ = sm.monitor()
    return

def run_shop(args):
    logger.warn('Shop only mode.')

    config_loader = ConfigLoader(test=args['test'])
    ss = SupremeShopper(config_loader,
                        autofill_on=args['autofill_on'],
                        keywords=args['keywords'],
                        size=args['size'],
                        refresh_time=args['refresh_time'],
                        recaptcha=args['recaptcha'])
    ss.run()
    return

if __name__ == '__main__':
    with open('config/base.yaml', 'r') as f:
        base = yaml.load(f)

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mode", dest='mode', default='both', help='`monitor`, `shop`, or `both`')
    parser.add_argument("--test", dest="test", default=False, action='store_true')

    args = vars(parser.parse_args())
    if args['test']:
        args.update(base['test'])
    else:
        args.update(base['real'])


    if args['mode'] == 'both':
        run_both_jobs(args)
        logger.warn('Shop complete. The web window will close in 100s, make sure you finish everything.')
        time.sleep(100)

    elif args['mode'] == 'monitor':
        run_monitor(args)

    elif args['mode'] == 'shop':
        run_shop(args)
        logger.warn('Shop complete. The web window will close in 100s, make sure you finish everything.')
        time.sleep(100)
    else:
        logger.warn('Unkown mode {}. Do nothing.'.format(args['mode']))