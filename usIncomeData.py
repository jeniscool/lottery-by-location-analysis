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

# root logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# file handler
fh = logging.FileHandler("logs/us-income-data.log", "w")
fh.setLevel(logging.DEBUG)
log.addHandler(fh)

# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
log.addHandler(sh)

class USIncomeData:

    ''' Constructor that takes no arguments. Calls the _load_data method '''
    def __init__(self):
        self.data = []
        self._load_data()

    ''' Methods to make the class iterable. Returns an iterator over the data list. '''
    def __iter__(self):
        self._iter=0
        return(self)

    def __next__(self):
        if self._iter == len(self.data):
            raise StopIteration
        ret = self.data[self._iter]
        self._iter += 1
        return ret

    ''' Method that will load the cleaned data file (auto-mpg.clean.txt) and
    instantiate AutoMPG objects and add them to the data attribute.
    This method calls _clean_data if the clean data file does not exist.
    (Hint: Use os.path.exists to check this.) '''
    def _load_data(self):

        # now the file exists
        log.debug(f"Importing us-income-data.csv...")
        with open('data/us-income-data.csv', encoding="ISO-8859-1") as file:
            reader = csv.reader(file, delimiter = ',',
                skipinitialspace=True)
            # declare namedtuple
            Record = namedtuple('Record', ['id','State_Code','State_Name',
            'State_ab','County','City','Place','Type','Primary','Zip_Code',
            'Area_Code','ALand','AWater','Lat','Lon','Mean','Median','Stdev','sum_w'])

            first_row_skipped = False
            for row in reader:
                # skip the first row
                if not first_row_skipped:
                    first_row_skipped = True
                    continue

                # create a Record passing in contents of a row
                record = Record(*row)
                # get fields to pass into AutoMPG
                state = record.State_Name
                city = record.City
                area = float(record.ALand) + float(record.AWater)
                avg_income = float(record.Mean)
                num_households = float(record.sum_w)

                # append AutoMPG to dictionary
                self.data.append(City(city, state, area, avg_income, num_households))

        self._condense_data()


    def _condense_data(self):

        data_dict = {}

        for city in self.data:
            key = f"{city.city},{city.state}"

            if key in data_dict:
                data_dict[key][0].append(city.area)
                data_dict[key][1].append(city.avg_income)
                data_dict[key][2].append(city.num_households)
            else:
                data_dict[key] = [[city.area], [city.avg_income], [city.num_households]]

        new_data_list = []
        for key in data_dict:
            area = np.array(data_dict[key][0]).sum()
            avg_income = np.array(data_dict[key][1]).mean()
            num_households = np.array(data_dict[key][2]).sum()

            # Grab City, State from key value
            name = key.split(",")
            city = name[0]
            state = name[1]

            if state != 'Puerto Rico':
                new_data_list.append(City(city, state, area, avg_income, num_households))

        self.data = new_data_list

    ''' Sorting functions '''
    def sort_by_alphabet(self):
        self.data.sort()
        log.debug(f"US income data sorted alphabeticaly.")

    def sort_by_size(self):
        self.data.sort(key=lambda obj: obj.area)
        log.debug(f"US income data sorted by size.")

    def sort_by_income(self):
        self.data.sort(key=lambda obj: obj.avg_income)
        log.debug(f"US income data sorted by income.")
