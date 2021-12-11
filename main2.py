"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""
import math
import statistics

import plotly.graph_objects as go
from countries import Country
from scrapy.crawler import CrawlerProcess
from factors2 import FoodInsecurity, FoodSecurity, get_confirmed_cases

food_insecurity = FoodInsecurity()
food_insecurity.calculate_food_insecurity()

CANADA = Country('Canada', food_insecurity.percentages)
USA = Country('United States', food_insecurity.percentages)
UAE = Country('United Arab Emirates', food_insecurity.percentages)
FRANCE = Country('France', food_insecurity.percentages)
CHINA = Country('China', food_insecurity.percentages)
JAPAN = Country('Japan', food_insecurity.percentages)
AUSTRALIA = Country('Australia', food_insecurity.percentages)
UK = Country('United Kingdom', food_insecurity.percentages)

COUNTRIES = [CANADA, USA, UAE, FRANCE, CHINA, JAPAN, AUSTRALIA, UK]


def data_cases_vs_fi() -> dict[str, tuple[float, float]]:
    """Return the data for the plot graphing confirmed cases vs food insecurity levels for each
    country.

    Preconditions
        - this function is only run once
    """
    confirmed_cases = get_confirmed_cases()

    # ACCUMULATOR data_so_far: the data of confirmed cases and food insecurity for each country,
    # so far
    data_so_far = {}
    countries = [key for key in food_insecurity.percentages]

    for country in countries:
        if country in confirmed_cases:
            x, y = confirmed_cases[country], food_insecurity.percentages[country]
            data_so_far[country] = (x, y)

    return data_so_far


def plot_cases_vs_fi() -> None:
    """Graph the data for confirmed cases to food insecurity."""
    data = data_cases_vs_fi()
    x_coords = []
    y_coords = []
    countries = []

    for country in data:
        x_coords.append(data[country][0] / 100)
        y_coords.append(data[country][1] / 100)
        countries.append(country)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        text=countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:.1%}<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'y': 0.92, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Food Insecurity (%)')

    fig.show()


def plot_cases_vs_fi_countries() -> None:
    """Graph the data for confirmed cases to food insecurity for specific countries."""
    data = data_cases_vs_fi()
    values = []

    # for country in COUNTRIES:
    #     x_values.append(data[country][0])
    #     y_values.append(data[country][1])
    #     countries_so_far.append(country)

    for country in COUNTRIES:
        x, y, c = data[country.name][0], data[country.name][1], country.name
        values.append((x, y, c))

    values.sort()

    x_values = [value[0] / 100 for value in values]
    y_values = [value[1] / 100 for value in values]
    countries_so_far = [value[2] for value in values]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        text=countries_so_far,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:.1%}<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity',
                             'y': 0.92, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Food Insecurity (%)')

    fig.show()


def plot_cases_to_unemployment() -> None:
    """Create graph of Confirmed Cases vs. Unemployment rate"""
    data = [(country.confirmed_cases, country.unemployment, country.name)
            for country in COUNTRIES]

    data.sort()

    x_values = [country[0] / 100 for country in data]
    y_values = [country[1] / 100 for country in data]
    names = [country[2] for country in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        text=names,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Unemployment: %{y:.1%}<br>' +
                      '<extra></extra>'
    ))

    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Unemployment',
                             'y': 0.92, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      xaxis_title='Confirmed Cases (%)',
                      yaxis_title='Unemployment (%)')

    # Line of best fit
    lobf_x_values = []
    lobf_y_values = []

    # slope = (len(COUNTRIES) * sum(x * y for x in x_values for y in y_values)
    #          - (sum(x_values) * sum(y_values))) / (len(COUNTRIES) * sum(x ** 2 for x in x_values)
    #                                                - (sum(x_values)) ** 2)
    slopes = []
    for i in range(len(x_values) - 1):
        slopes.append((x_values[i + 1] - x_values[i]) / (y_values[i + 1] - y_values[i]))
    slope = statistics.mean(slopes)
    y_intercept = (sum(y_values) - (slope * (sum(x_values)))) / len(COUNTRIES)

    # For a meaningful LOBF
    max_unemployment = max(country.unemployment for country in COUNTRIES) / 100
    max_confirmed_cases = max(country.confirmed_cases for country in COUNTRIES)

    for x in range(0, math.ceil(max_confirmed_cases) * 100, 1):  # * 100 for more points...
        y = slope * (x / 10000) + y_intercept
        if 0 < y < max_unemployment * 1.5:  # * 1.5 for a bit more insight
            lobf_x_values.append(x / 10000)
            lobf_y_values.append(y)

    fig.add_trace(go.Scatter(
        x=lobf_x_values,
        y=lobf_y_values,
        mode='lines',
        name='Line of Best Fit',
        hovertemplate='<b>Line of Best Fit</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Unemployment: %{y:.1%}<br>' +
                      '<extra></extra>',
        line=dict(color='firebrick', width=2)
    ))

    fig.show()


if __name__ == '__main__':
    process = CrawlerProcess(settings={'FEEDS': {'food_security.json': {'format': 'json',
                                                                        'overwrite': True}, },
                                       'LOG_ENABLED': False})
    process.crawl(FoodSecurity)
    process.start()

    # plot_cases_vs_fi()
    # plot_cases_vs_fi_countries()
    # plot_cases_to_unemployment()

    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['python_ta.contracts', 'factors'],
    #     'disable': ['R1705', 'C0200', 'E9998', 'E9999'],
    # })
    #
    # import python_ta.contracts
    #
    # python_ta.contracts.DEBUG_CONTRACTS = False
    # python_ta.contracts.check_all_contracts()
    #
    # import doctest
    #
    # doctest.testmod()
