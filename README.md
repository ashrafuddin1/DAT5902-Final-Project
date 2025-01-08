# DAT5902-Final-Project

This project analyses the relationship between GDP per capita and Population with CO₂ emissions for countries in 2022 using data visualisation. It highlights key insights like the carbon efficiency of countries with respect to their economic output.

# Features
- Data preparation and cleaning
- Categorisation of countries into income groups
- Calculation of CO₂ emissions per $100,000 GDP
- Visualisation:
  - Scatter plot of GDP per capita vs CO₂ emissions per capita with income group categorisation and population based point sizes
  - 10 least carbon-efficient countries w.r.t GDP (bar plot)
  - 10 most carbon-efficient countries w.r.t GDP (bar plot)
- Analysis:
  - Regression analysis of scatter plot with calculated gradient and y-intercept
  - Pearson correlation coefficients for various pairs of variables

# Project Structure 
📂 DAT5902-FINAL-PROJECT/ 
├──| _pycache_ 
   ├── analysis.cpython-311.pyc
   ├── headline_figure_code.cpython-311.pyc
├──| .circleci 
   ├── config.yml # config file for Circle CI unit tests
├── analysis.py # Main code for figures and analysis 
├── bottom10_figure.png # Bottom 10 barplot (generated)
├── co2-emissions-vs-gdp.csv # Dataset 
├── headline_figure.png # Scatter plot (generated)
├── README.md # Documentation (this file)
├── requirements.txt # List of dependencies for unit tests
├── test_data.csv # Mock data for the unit tests
├── unittests.py # Unit tests for functions 
├── top10_figure.png # Top 10 barplot (generated)  
├── unittests_to_pass.txt # Outline of unit tests
└── unittests.py # Test suite for functions

*Setup and Installation* Clear instructions to set up the environment and run the project.

1. This project requires Python 3.8+ and the following dependencies to be installed:

  -pytest
  -unittest
  -matplotlib
  -seaborn
  -scipy
  -numpy
  -pandas

2. Run analysis.py

The following plots will be saved in the current directory:

headline_figure.png
top10_figure.png
bottom10_figure.png

The quantitative analysis will be printed in the terminal

3. Run unittests.py to verify the functions

# Usage

## Functions
#### Data Preparation
prepare_data(filepath): Cleans the dataset and removes unnecessary columns.

#### Filtering
filter_by_2022(dateframe): Filters data to include only 2022 records.

#### Income Group Classification
add_income_group(dataframe): Adds an income group column based on GDP per capita.

#### Efficiency Calculation
add_emissions_per_gdp(dataframe): Calculates CO₂ emissions per $100,000 GDP.

#### Visualisation
create_highlight_plot(dataframe, highlight_countries, bubble_size): Creates a scatter plot with annotations for specific countries, regression line and population based point sizes for countries
create_top_10_barplot(dataframe): Generates a bar plot for the least carbon-efficient countries.
create_bottom_10_barplot(df): Generates a bar plot for the most carbon-efficient countries.

#### Visualisations
Scatter Plot: Highlights relationships between GDP per capita, Population and CO₂ emissions.
Bar Plots: Showcases the most and least carbon-efficient countries based on CO₂ emissions relative to economic output.


# Dataset 

Source: It can be found in the co2-emissions-vs-gdp.csv file in this directory or from https://ourworldindata.org/grapher/co2-emissions-vs-gdp.csv?v=1&csvType=full&useColumnShortNames=false

Description:
Entity: Name of the country
Year: Year of the data
GDP per capita: GDP per capita in USD
Annual CO₂ emissions (per capita): CO₂ emissions per capita in tonnes
Population (historical): Population size of the country

Other columns are disregarded as not relevant to the scope of this project

# Testing

Details of unit testing can be found in unittests_to_pass.txt
Test suite is unittests.py

# Acknowledgments

I acknowledge the dataset used is from Our World In Data who originally obtained it from the Global Carbon Budget. 

Citation: Global Carbon Budget (2024)Population based on various sources (2024)Bolt and van Zanden - Maddison Project Database 2023HYDE (2023)Gapminder - Population v7 (2022)UN, World Population Prospects (2024)Gapminder - Systema Globalis (2022)Our World in Data – with major processing by Our World In Data

I acknowledge the use of the following Python libraries/frameworks for the purpose of the analysis in this project:

  -pytest
  -unittest
  -matplotlib
  -seaborn
  -scipy
  -numpy
  -pandas