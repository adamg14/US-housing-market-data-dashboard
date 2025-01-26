# United States Housing Market Data Dashboard

## Overview

The US housing market data dashboard aims to:
- Understand historical and current trends in the US housing market
- Analyse various metrics such as average home price, rent price and sales
- Comparing regional differences in housing data across different states

Housing market data is a valuable resource for real estate professionals, economists and prospective buyers. By presenting the data via a shiny for python dashboard in a clear, visual format the aim is to make the housing market insights more accessible.

## Features

- __Interactive Dashboard:__ Exploring housing trends over time by adjusting filters e.g. state and date range
- __Multiple Visualisations:__ Separate charts for the different housing market metrics to help interpret market data.
- __Data Cleaning & Analysis:__ Functions taking in the raw .csv file data and performing actions like type casting to format the data in the correct manner to be displayed.

## Dataset
- __Source:__ [Housing Market Data Source](https://www.zillow.com/research/data/)
- _File Format:__ .csv

## Project Structure
- ./UNITED_STATES.py = List of the states within America for the user to be able to filter.
- ./app.py = The Shiny for Python data dashboard
- ./data_aggregation.py = Functions calculating the data aggregation of the different metrics provided by the dashboard, optionally filtering by state.
- ./data_visualisation.py = Data cleaning and type casting

## Getting Started
1. Clone the git repository
```bash
git clone https://github.com/adamg14/US-housing-market-data-dashboard.git
cd US-housing-market-data-dashboard
```

2. Install the dependencies
```bash
pip install pandas numpy shiny seaborn matplotlib faicons
```

3. Run the shiny application for the dashboard to be rendered on localhost:3000
```bash
shiny run app.py
```


