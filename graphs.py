"""The Threat of Food Insecurity in Canada from the Economic Fallout of COVID-19

Instructions
============

This Python module contains the main functions and blocks of code required to run the entire
program. This module will load the necessary files from the datasets, perform computations on
the data, and produce an interactive graph in your browser. (SUBJECT TO CHANGE)
"""

import plotly.graph_objects as go
from factors import get_food_insecurity, get_confirmed_cases

COUNTRIES = ['Canada', 'United States', 'China', 'Japan', 'Australia', 'France',
             'United Arab Emirates', 'United Kingdom']


def data_cases_vs_fi() -> dict[str, tuple[float, float]]:
    """Return the data for the plot graphing confirmed cases vs food insecurity levels for each
    country.

    Preconditions
        - this function is only run once
    """
    food_insecurity = get_food_insecurity()
    confirmed_cases = get_confirmed_cases()

    # ACCUMULATOR data_so_far: the data of confirmed cases and food insecurity for each country,
    # so far
    data_so_far = {}
    countries = [key for key in food_insecurity]

    for country in countries:
        if country in confirmed_cases:
            x, y = confirmed_cases[country], food_insecurity[country]
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
        x, y, c = data[country][0], data[country][1], country
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
