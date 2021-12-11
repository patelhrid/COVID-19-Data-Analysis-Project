"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""

from countries import Country
from scrapy.crawler import CrawlerProcess
from factors import FoodSecurity, FoodInsecurity

food_insecurity = FoodInsecurity()
food_insecurity.calculate_food_insecurity()

CANADA = Country('Canada', food_insecurity)
USA = Country('United States', food_insecurity)


if __name__ == '__main__':
    process = CrawlerProcess(settings={'FEEDS': {'food_security.json': {'format': 'json',
                                                                        'overwrite': True}, },
                                       'LOG_ENABLED': False})
    process.crawl(FoodSecurity)
    process.start()
