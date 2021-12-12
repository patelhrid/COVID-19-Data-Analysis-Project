"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce interactive graphs in your browser.
"""

from scrapy.crawler import CrawlerProcess
from factors3 import FoodSecurity, FoodInsecurity
import graphs3


def run_graph() -> None:
    """Generate a graph showing the food insecurity, confirmed cases, and different factors."""
    graphs3.plot_cases_vs_food_insecurity(food_insecurity)
    graphs3.plot_cases_vs_unemployment(food_insecurity)
    graphs3.plot_cases_vs_cpi(food_insecurity)
    graphs3.plot_cases_vs_income_plot(food_insecurity)


if __name__ == '__main__':
    process = CrawlerProcess(settings={'FEEDS': {'food_security.json': {'format': 'json',
                                                                        'overwrite': True}, },
                                       'LOG_ENABLED': False})
    process.crawl(FoodSecurity)
    process.start()

    food_insecurity = FoodInsecurity()
    food_insecurity.calculate_food_insecurity()
