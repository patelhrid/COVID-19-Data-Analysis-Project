"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""

import csv
from factors import ConfirmedCases, Unemployment, unemployment


class Country:
    """A class representing a country, along with several factors related ot the
    pandemic.

    Instance Attributes:
        - name: the name of the country
        - population: the total population of the country
        - food_insecurity: the percent of the country's population that is food insecure
        - confirmed cases: the amount of confirmed COVID-19 cases as a percent of the population
        - unemployment: the unemployment rate of the country, as a percentage
        - cpi: the consumer price index for food, as a percentage
        - income: the average income of the country
    """
    name: str
    population: int
    food_insecurity: float
    confirmed_cases: ConfirmedCases()
    unemployment: float
    cpi: float
    income: float
    # conversion:

    def __init__(self, name: str) -> None:
        """Initialize the attributes of Country."""
        self.name = name
        self.population = ppln(self.name)
        self.food_insecurity = 0
        self.confirmed_cases = ConfirmedCases()
        self.unemployment = unemployment(self.name)
        self.cpi = 0
        self.income = 0
        # self.conversion = ...

        self.confirmed_cases.calculate_percent(self.name, self.population)

    # def calculate_confirmed_cases(self) -> None:
    #     """Update the amount of confirmed cases of the country, as a percentage."""
    #     self.confirmed_cases.calculate_percent(self.name, self.population)


# remove
class Canada(Country):
    """A concrete class representing the country Canada.

    Instance Attributes:
        - name: the name of the country
        - population: the total population of the country
        - food_insecurity: the percent of the country's population that is food insecure
        - confirmed cases: the amount of confirmed COVID-19 cases as a percent of the population
        - unemployment: the unemployment rate of the country, as a percentage
        - cpi: the consumer price index for food, as a percentage
        - income: the average income of the country
    """
    name: str
    population: int
    food_insecurity: float
    confirmed_cases: ConfirmedCases()
    unemployment: float
    cpi: float
    income: float

    def __init__(self) -> None:
        """Initialize the attributes of Canada."""
        self.name = 'Canada'
        Country.__init__(self, self.name)
        self.food_insecurity = 0
        self.confirmed_cases = ConfirmedCases()
        self.unemployment = 0
        self.cpi = 0
        self.income = 0

        self.calculate_confirmed_cases()

    def calculate_confirmed_cases(self) -> None:
        """Update the amount of confirmed cases of the country, as a percentage."""
        self.confirmed_cases.calculate_percent(self.name, self.population)


def ppln(country: str) -> int:
    """Return the population of the country from a dataset.

    # Preconditions:
    #     - the second last row for each country is the population in 2020
    """
    filename = 'datasets/API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv'
    total_population = 0
    with open(filename) as f:
        # skip the first 5 lines
        reader = csv.reader(f, delimiter=',')
        _ = [next(reader) for _ in range(5)]

        for row in reader:
            current_country = row[0]
            if country == current_country:
                total_population = int(row[-2])

    return total_population




# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'extra-imports': ['python_ta.contracts', 'factors'],
#         'disable': ['R1705', 'C0200', 'E9998', 'E9999'],
#     })
#
#     import python_ta.contracts
#
#     python_ta.contracts.DEBUG_CONTRACTS = False
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#
#     doctest.testmod()
