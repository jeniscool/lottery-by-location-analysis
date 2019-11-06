import os
from collections import namedtuple, defaultdict
import csv
import logging
import argparse
import sys
import requests
import numpy as np
import matplotlib.pyplot as plt
from usCity import City
from usIncomeData import USIncomeData

# root logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# file handler
fh = logging.FileHandler("logs/main.log", "w")
fh.setLevel(logging.DEBUG)
log.addHandler(fh)

# parsing arguments
parser = argparse.ArgumentParser(description='analyze US Household Incomes data set')
parser.add_argument('-s', '--sort', default='alphabetical', metavar='<sort order>',
                    choices=['alphabetical', 'size', 'income'])
parser.add_argument('-o', '--ofile', metavar='<outfile>', default='sys.stdout')
parser.add_argument('-p', '--plot', action='store_true', help='graphical output')
parser.add_argument('command', metavar = '<command>', type = str,
                    choices = ['print', 'mpg_by_year', 'mpg_by_make'],
                    help='command to execute')
args = parser.parse_args()

if __name__ == '__main__':

    log.debug(f"Arguments: {args}")

    us_income_data = USIncomeData()

    if args.command == 'print': # insure print is our command

        # if plot option chosen, exit system.
        if args.plot:
            log.info(f"Error: '--plot' argument must be accompanied by 'mpg_by_year' or 'mpg_by_make' command")
            log.debug(f"Exiting program.")
            sys.exit(1)

        log.debug("Begin printing data...")
        # apply sort options
        if args.sort == 'alphabet':
            us_income_data.sort_by_alphabet()
        elif args.sort == 'size':
            us_income_data.sort_by_alphabet()
            us_income_data.sort_by_size()
        elif args.sort == 'income':
            us_income_data.sort_by_alphabet()
            us_income_data.sort_by_income()

        log.debug(f"Printing to {args.ofile}...")
        # if ofile not specified, print to commandline
        if args.ofile == 'sys.stdout':
            for city in us_income_data:
                log.info(city)
        # else, write to file
        else:
            with open(args.ofile, 'w') as o:
                writer = csv.writer(o, delimiter=',')
                for city in us_income_data:
                    writer.writerow([city.state, city.city, city.area, city.avg_income, city.num_households])
            log.debug(f"Closing {args.ofile}...")


    else:
        log.info(f"Do this later")
