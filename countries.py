"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""

import csv
import factors


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
    confirmed_cases: float
    unemployment: float
    cpi: float
    income: float

    def __init__(self, name: str, food_insecurity_dict: dict) -> None:
        """Initialize the attributes of Country."""
        self.name = name
        self.population = ppln(self.name)
        self.food_insecurity = food_insecurity_dict[self.name]
        self.confirmed_cases = factors.get_confirmed_cases()[self.name]
        self.unemployment = factors.get_unemployment(self.name)
        self.cpi = factors.get_cpi_average(self.name)
        self.income = factors.get_income(self.name)


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
            if country in current_country:
                total_population = int(row[-2])
            elif (country == 'United States'
                  or country == 'United States of America'
                  or country == 'USA') \
                    and (row[1] == 'United States'
                         or row[1] == 'United States of America'
                         or row[1] == 'USA'):
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
