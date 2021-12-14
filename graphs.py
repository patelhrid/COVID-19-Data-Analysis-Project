"""Graphing Confirmed COVID-19 Cases, Food Insecurity, and Other Economic Factors

Description
============

This Python module contains the functions that will create the plots of our datasets using plotly.
There are 8 main countries whose data is being plotted: Canada, United States, France, Germany,
Japan, South Korea, Australia, and United Kingdom.

There are 5 plots with the independent variable as the percent of confirmed COVID-19 cases in
each country. The first dependent variable is Food Insecurity for all countries whose data was
available. The rest focus on the 8 countries listed above: Food Insecurity, Unemployment,
Consumer Price Index, and Income.
"""
import plotly.graph_objects as go
from countries import Country
from factors import FoodInsecurity, get_confirmed_cases


def plot_graph(food_insecurity: FoodInsecurity) -> None:
    """Graph the data for confirmed cases to food insecurity for all countries and
    specific countries, with traces for each set of data.

    Preconditions
        - food_insecurity.index != {}
    """

    # Create the 8 countries as Country objects and get the data for confirmed cases
    countries = create_countries(food_insecurity)
    confirmed_cases = get_confirmed_cases()

    # FOOD INSECURITY PLOTS
    all_fi_data = data_fi_all(food_insecurity, confirmed_cases)
    all_food_insecurity_plot = plot_fi_all(all_fi_data[0], all_fi_data[1], all_fi_data[2])
    all_food_insecurity_lobf = get_lobf(all_fi_data[0], all_fi_data[1])

    food_insecurity_plot, food_insecurity_lobf = get_graphs('Food Insecurity', countries)

    # UNEMPLOYMENT, CPI, AND INCOME PLOTS
    unemployment_plot, unemployment_lobf = get_graphs('Unemployment', countries)
    cpi_plot, cpi_lobf = get_graphs('Consumer Price Index', countries)
    income_plot, income_lobf = get_graphs('Income', countries)

    # Create the plot and add traces for each graph
    fig = go.Figure()
    fig.add_trace(all_food_insecurity_plot)     # Trace 1
    fig.add_trace(all_food_insecurity_lobf)     # Trace 2
    fig.add_trace(food_insecurity_plot)         # Trace 3
    fig.add_trace(food_insecurity_lobf)         # Trace 4
    fig.add_trace(unemployment_plot)            # Trace 5
    fig.add_trace(unemployment_lobf)            # Trace 6
    fig.add_trace(cpi_plot)                     # Trace 7
    fig.add_trace(cpi_lobf)                     # Trace 8
    fig.add_trace(income_plot)                  # Trace 9
    fig.add_trace(income_lobf)                  # Trace 10

    # Change the initial titles of the plots
    fig.update_layout(title={'text': 'Confirmed COVID-19 Cases vs Food Insecurity in 2020 (All)',
                             'y': 0.932, 'x': 0.46, 'xanchor': 'center', 'yanchor': 'top',
                             'font': {'size': 25}},
                      xaxis_title='Total Confirmed Cases (% of population)',
                      yaxis_title='Food Insecurity Index',
                      legend={'font_size': 15})

    # Create buttons to toggle between the plots
    # The values in args correspond to each trace of fig: [Trace 1, Trace 2, Trace 3, ...] and so on
    fig.update_layout(updatemenus=[
        # Buttons for food insecurity plots
        dict(type='buttons',
             direction='left',
             x=0, y=1.07,
             xanchor='left', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='All Countries',
                      method='update',
                      args=[{'visible': [True, 'legendonly', False, False, False,
                                         False, False, False, False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity in 2020 (All)',
                             'xaxis': {'title': 'Total Confirmed Cases (% of population)'},
                             'yaxis': {'title': 'Food Insecurity Index'},
                             'font': {'size': 15},
                             }]),
                 dict(label='8 Countries',
                      method='update',
                      args=[{'visible': [False, False, True, 'legendonly', False,
                                         False, False, False, False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Food Insecurity in 2020',
                             'xaxis': {'title': 'Total Confirmed Cases (% of population)'},
                             'yaxis': {'title': 'Food Insecurity Index'},
                             'font': {'size': 15}
                             }]),
             ]), ),

        # Buttons for economic factors plots
        dict(type='buttons',
             direction='left',
             x=1, y=1.07,
             xanchor='right', yanchor='top',
             font={'size': 14},
             buttons=list([
                 dict(label='Unemployment',
                      method='update',
                      args=[{'visible': [False, False, False, False, True, 'legendonly',
                                         False, False, False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs Unemployment in 2020',
                             'xaxis': {'title': 'Total Confirmed Cases (% of population)'},
                             'yaxis': {'title': 'Average Unemployment Rate (%)'},
                             'font': {'size': 15},
                             }]),
                 dict(label='CPI',
                      method='update',
                      args=[{'visible': [False, False, False, False, False,
                                         False, True, 'legendonly', False, False]},
                            {'title': 'Confirmed COVID-19 Cases vs CPI in 2020',
                             'xaxis': {'title': 'Total Confirmed Cases (% of population)'},
                             'yaxis': {'title': 'Average Consumer Prices, Food Indices'},
                             'font': {'size': 15}
                             }]),
                 dict(label='Income',
                      method='update',
                      args=[{'visible': [False, False, False, False, False,
                                         False, False, False, True, 'legendonly']},
                            {'title': 'Confirmed COVID-19 Cases vs Income in 2020',
                             'xaxis': {'title': 'Total Confirmed Cases (% of population)'},
                             'yaxis': {'title': 'Average Income Levels (USD)'},
                             'font': {'size': 15}
                             }]),
             ]), )
    ])

    # Add labels for the buttons
    fig.update_layout(annotations=[
        dict(text='Food Insecurity:', showarrow=False, x=0, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15),
        dict(text='Economic Factors:', showarrow=False, x=1, y=1.107, yref='paper', xref='paper',
             visible=True, font_size=15)
    ])

    # Adjust size for x and y axes
    fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(size=18)))
    fig.for_each_yaxis(lambda axis: axis.title.update(font=dict(size=18)))

    # Display the graph
    fig.show()


def get_graphs(factor: str, countries: list[Country]) -> list[go.Scatter]:
    """Return a list of scatter plots displaying the factor data for countries. The first is the
    main plot, and the second is the line of best fit plot.

    Preconditions
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    # Unpack the data
    x, y, c = get_data(countries, factor)

    # Create and return the 2 plots
    main_plot = get_plot(x, y, c, factor)
    line_of_best_fit = get_lobf(x, y)
    return [main_plot, line_of_best_fit]


def get_plot(x_values: list[float], y_values: list[float], countries: list[Country], factor: str) \
        -> go.Scatter:
    """Return a scatter plot displaying data for factor, plotting each value in x_values and
    y-values for their corresponding country in countries.

    Preconditions:
        - x_values != []
        - y_values != []
        - len(x_values) == len(y_values)
        - countries != []
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    # Assign the unit displayed in the hover text of the graph ($, %, etc.)
    if factor == 'Income':
        unit = '{y:$,.2f}'
    elif factor == 'Unemployment':
        unit = '{y:.2%}'
    else:
        unit = '{y:.2f}'

    # Create the plot
    plot = go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Data',
        text=countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      f'{factor}'': %'f'{unit}''<br>' +
                      '<extra></extra>',
        showlegend=True,
        visible=False
    )

    return plot


def get_lobf(x_values: list[float], y_values: list[float]) -> go.Scatter:
    """Return a line plot with the line of best fit, given x_values and y_values.

    Equation for line of best fit (least square method):
    Let x1 and y1 be each coordinate in the data, X and Y be the means of the x-values and y-values.
        slope = summation((x1 - X)(y1 - y)) / summation((x1 - X)^2),
        y_intercept = Y - slope * x

    Preconditions:
        - x_values != []
        - y_values != []
        - len(x_values) == len(y_values)
    """
    # Calculate the slope and y-intercept for the line of best fit
    # ACCUMULATORS: the numerator and denominator of the equation for line of best fit so far
    numerator_so_far = 0
    denominator_so_far = 0

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    for i in range(len(x_values)):
        numerator_so_far += (x_values[i] - x_mean) * (y_values[i] - y_mean)
        denominator_so_far += (x_values[i] - x_mean) ** 2

    slope = numerator_so_far / denominator_so_far
    y_intercept = y_mean - slope * x_mean

    # Generate points for the line of best fit
    # ACCUMULATORS: the line of best fit coordinates so far
    lobf_x_values = []
    lobf_y_values = []

    for x in x_values:
        lobf_x_values.append(x)
        lobf_y_values.append(slope * x + y_intercept)

    # If the line of best fit is for the graph returned from plot_fi_all, make the visibility
    #  'legendonly' so it is not initially displayed when the figure is first opened
    if len(x_values) > 8:
        visibility = 'legendonly'
    else:
        visibility = False

    lobf = go.Scatter(
        x=lobf_x_values,
        y=lobf_y_values,
        mode='lines',
        name='Line of Best Fit',
        line=dict(color='firebrick', width=2),
        showlegend=True,
        visible=visibility,
        hoverinfo='skip'
    )

    return lobf


def get_data(countries: list[Country], factor: str) -> list[list]:
    """Return the data for the plot showing the 8 specific countries. The data returned is a
    list of x-values as the confirmed cases, y-values as the factor values, and country names.

    Preconditions
        - countries is the list returned from the create_countries function
        - factor in ['Food Insecurity', 'Unemployment', 'Consumer Price Index', 'Income']
    """
    # Get the proper y-values, depending on the factor input
    # Dividing some values by 100 to get decimal values that will later be converted to
    # percentages in the hover text on the plot
    if factor == 'Food Insecurity':
        data = [(country.confirmed_cases, country.food_insecurity, country.name)
                for country in countries]
    elif factor == 'Unemployment':
        data = [(country.confirmed_cases, country.unemployment / 100, country.name)
                for country in countries]
    elif factor == 'Consumer Price Index':
        data = [(country.confirmed_cases, country.cpi, country.name)
                for country in countries]
    else:  # factor == 'Income'
        data = [(country.confirmed_cases, country.income, country.name)
                for country in countries]
    data.sort()

    # Unpacking the data for the 8 specific countries
    x_values = [value[0] / 100 for value in data]
    y_values = [value[1] for value in data]
    countries = [value[2] for value in data]

    return [x_values, y_values, countries]


def plot_fi_all(x_values: list[float], y_values: list[float], countries: list[str]) -> go.Scatter:
    """Return a scatter plot displaying confirmed_cases as the x-values and food insecurity as the
    y-values for all available countries.

    Preconditions:
        - x_values != []
        - y_values != []
        - len(x_values) == len(y_values)
        - countries != []
        - data for food insecurity and confirmed cases is available for each country in countries
    """
    plot = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        name='Data',
        text=countries,
        hovertemplate='<b>%{text}</b><br><br>' +
                      'Confirmed Cases: %{x:.2%}<br>' +
                      'Food Insecurity: %{y:}<br>' +
                      '<extra></extra>',
        showlegend=True,
        visible=True
    )

    return plot


def data_fi_all(food_insecurity: FoodInsecurity, confirmed_cases: dict[str, float]) -> list[list]:
    """Return the data for the plot graphing confirmed cases vs food insecurity levels for all
    available countries as a list of x-values as the confirmed cases, y-values as the food
    insecurity level, and country names (strings).

    Preconditions
        - food_insecurity.index != {}
        - confirmed_cases != {}
    """
    # ACCUMULATORS: the data for confirmed cases and food insecurity so far
    x_values = []
    y_values = []
    countries_so_far = []

    countries = [key for key in food_insecurity.index]

    for country in countries:
        # Only get data for the countries in both food_insecurity.index and confirmed_cases
        if country in confirmed_cases:
            x_values.append(confirmed_cases[country] / 100)
            y_values.append(food_insecurity.index[country])
            countries_so_far.append(country)

    return [x_values, y_values, countries_so_far]


def create_countries(food_insecurity: FoodInsecurity) -> list[Country]:
    """Return a list of 8 Country objects that will be plotted on the graph.

    Preconditions
        - food_insecurity.index != {}
        - data for the Country attributes is available for each Country made
    """
    canada = Country('Canada', food_insecurity)
    usa = Country('United States', food_insecurity)
    france = Country('France', food_insecurity)
    germany = Country('Germany', food_insecurity)
    korea = Country('South Korea', food_insecurity)
    japan = Country('Japan', food_insecurity)
    australia = Country('Australia', food_insecurity)
    uk = Country('United Kingdom', food_insecurity)

    return [canada, usa, japan, korea, australia, uk, germany, france]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'plotly.graph_objects', 'countries', 'factors'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'E9989', 'R1721'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
