"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""

from countries import Country
from factors import get_food_insecurity

# Since scrapy can only run once
all_food_insecurity = get_food_insecurity()

# All countries as Country objects, with their respective statistics
CANADA = Country('Canada', all_food_insecurity)
USA = Country('United States', all_food_insecurity)
UAE = Country('United Arab Emirates', all_food_insecurity)
FRANCE = Country('France', all_food_insecurity)
CHINA = Country('China', all_food_insecurity)
JAPAN = Country('Japan', all_food_insecurity)
AUSTRALIA = Country('Australia', all_food_insecurity)
UK = Country('United Kingdom', all_food_insecurity)
