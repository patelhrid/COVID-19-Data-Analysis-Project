"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""
from factors import ppln, get_food_insecurity, get_confirmed_cases, get_unemployment, \
    get_cpi, get_income_usd, FoodInsecurity


# class FI:
#     """FI"""
#     fi: dict[str, float]
#
#     def __init__(self) -> None:
#         self.fi = FoodInsecurity.calculate_food_insecurity()

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
    # food_insecurity: float
    food_insecurity: float
    confirmed_cases: float
    unemployment: float
    # cpi: float
    income: float

    def __init__(self, name: str, fi: FoodInsecurity()) -> None:
        """Initialize the attributes of Country."""
        self.name = name
        self.population = ppln(self.name)
        # self.food_insecurity = get_food_insecurity()[self.name]
        self.food_insecurity = fi.percentages[self.name]
        self.confirmed_cases = get_confirmed_cases()[self.name]
        self.unemployment = get_unemployment(self.name)
        # self.cpi = get_cpi_average(self.name)
        self.income = get_income_usd(self.name)
        # self.conversion = ...

    # def


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
