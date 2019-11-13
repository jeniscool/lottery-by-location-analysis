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
                    choices=['alphabetical', 'size', 'income', 'population'])
parser.add_argument('-o', '--ofile', metavar='<outfile>', default='sys.stdout')
parser.add_argument('-p', '--plot', action='store_true', help='graphical output')
parser.add_argument('command', metavar = '<command>', type = str,
                    choices = ['print', 'plot'],
                    help='command to execute')
args = parser.parse_args()

def is_outlier(points, thresh=12):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


if __name__ == '__main__':

    log.debug(f"Arguments: {args}")

    us_income_data = USIncomeData()

    if args.command == 'print': # insure print is our command

        # if plot option chosen, exit system.
        if args.plot:
            log.info(f"Error: '--plot' argument must be accompanied by BLANK or BLANK command")
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
        elif args.sort == 'population':
            us_income_data.sort_by_alphabet()
            us_income_data.sort_by_population()

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

    elif args.command == 'plot':

        incomes = np.array([])
        areas = np.array([])
        population = np.array([])
        for city in us_income_data:

            incomes = np.append(incomes,city.avg_income)
            areas = np.append(areas,city.area)
            population = np.append(population,city.num_households)


        filter_income = is_outlier(incomes)
        filter_area = is_outlier(areas)
        print(f"{filter_income}, {filter_area}")

        x = []
        y = []

        for i in range(len(filter_income)):
            if not filter_income[i] and not filter_area[i]:
                x.append(incomes[i])
                y.append(areas[i])


        plt.scatter(x, y)
        plt.title('Average Income vs. Size of City')
        plt.xlabel('Average Household Income')
        plt.ylabel('Physical Size of City')
        plt.show()

        '''
        plt.scatter(incomes, population)
        plt.title('Average Income vs. Number of Households in City')
        plt.xlabel('Average Household Income')
        plt.ylabel('Number of Households')
        plt.show()

        plt.scatter(areas, population)
        plt.title('Size of City vs. Number of Households')
        plt.xlabel('Size of City')
        plt.ylabel('Number of Households')
        plt.show()
        '''


        # make plot of income by population

    else:
        log.info(f"Do this later")
