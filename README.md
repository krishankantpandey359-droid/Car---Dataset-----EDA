# Car Dataset Exploratory Data Analysis

## Project Overview

This project focuses on Exploratory Data Analysis (EDA) of a Cars dataset obtained from Kaggle. The analysis is performed using Python to understand the structure of the dataset, clean the data, identify patterns, detect outliers, and explore relationships between different car features.

The project covers data cleaning, statistical analysis, outlier detection, univariate analysis, bivariate analysis, aggregated analysis, and multivariate visualization.

## Problem Statement

The Cars dataset contains information about different car models and their features such as manufacturer, model, year, horsepower, cylinders, transmission, drive mode, fuel economy, and price.

The main objective of this project is to explore the dataset and understand the relationships between these features, especially the factors associated with car prices.

## Dataset

The dataset contains information about cars with features such as:

- Make
- Model
- Year
- Engine HP
- Engine Cylinders
- Transmission Type
- Driven Wheels
- Highway MPG
- City MPG
- MSRP

During data preprocessing, some unnecessary columns were removed and selected columns were renamed for better readability.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Data Cleaning and Preprocessing

The following data preprocessing steps were performed:

1. Loaded the Cars dataset into a Pandas DataFrame.
2. Checked the data types of the columns.
3. Removed unnecessary columns.
4. Renamed selected columns using clearer names.
5. Checked and removed duplicate records.
6. Checked for missing values.
7. Removed rows containing missing values.
8. Used statistical analysis to understand the numerical features.
9. Detected outliers using box plots.
10. Applied the IQR method for numerical outlier detection.

### Dataset Changes

- Rows before removing duplicates: **11,914**
- Rows after removing duplicates: **10,925**
- Rows after removing missing values: **10,827**
- Rows in the outlier-filtered dataframe: **9,191**

## Feature Changes

The following columns were removed during preprocessing:

- Engine Fuel Type
- Market Category
- Vehicle Style
- Popularity
- Number of Doors
- Vehicle Size

Some columns were also renamed:

| Original Column | New Column |
|---|---|
| Engine HP | HP |
| Engine Cylinders | Cylinders |
| Driven_Wheels | Drive Mode |
| MSRP | Price |

## Exploratory Data Analysis

### Univariate Analysis

Univariate analysis was performed to understand individual variables and their distributions.

The project includes:

- Histograms
- Density plots
- Box plots
- Bar charts
- Count plots

The distributions of numerical variables such as HP, Cylinders, Year, Highway MPG, City MPG, and Price were explored.

The distribution of car makes was also analyzed using a bar chart.

## Bivariate Analysis

Bivariate analysis was performed to understand relationships between two variables.

A scatter plot was used to analyze the relationship between:

**Horsepower (HP) and Price**

The correlation between HP and Price was approximately:

**0.660**

This indicates a positive relationship between horsepower and car price in this dataset.

## Aggregated Analysis

A bar plot was used to compare the average car price across different numbers of cylinders.

A count plot was also used to examine the number of cars by transmission type.

## Multivariate Analysis

A correlation heatmap was created to examine relationships between the numerical features in the dataset.

Some notable correlations include:

- HP and Price: **0.660**
- Cylinders and Price: **0.555**
- HP and Cylinders: **0.788**
- Highway MPG and City MPG: **0.841**
- Cylinders and City MPG: **-0.632**
- Cylinders and Highway MPG: **-0.612**

The heatmap provides a visual overview of the relationships between the numerical variables.

## Outlier Detection

Box plots were used to identify potential outliers in numerical variables such as Price and HP.

The Interquartile Range (IQR) method was then applied to identify observations outside the range:

- Lower Bound = Q1 - 1.5 × IQR
- Upper Bound = Q3 + 1.5 × IQR

A separate dataframe was created after filtering rows containing numerical outliers.

## Key Findings

Some important findings from the analysis are:

- The dataset contained duplicate records that were removed during preprocessing.
- Missing values were present in the HP and Cylinders columns and were removed.
- Car prices show a positive correlation with horsepower.
- Cars with more cylinders generally show higher average prices in the analyzed data.
- Horsepower and number of cylinders have a strong positive correlation.
- Highway MPG and City MPG have a strong positive correlation.
- Higher cylinder counts are negatively correlated with fuel economy variables such as Highway MPG and City MPG.
- The dataset contains several numerical outliers, which were identified using box plots and the IQR method.

## Visualizations

The project includes the following visualizations:

- Box Plot of Car Price
- Box Plot of Horsepower
- Histogram and Density Plot of Horsepower
- Distribution plots of numerical features
- Top Car Makes by Number of Cars
- Transmission Type by Drive Mode
- Horsepower vs Price Scatter Plot
- Average Price by Number of Cylinders
- Number of Cars by Transmission Type
- Correlation Heatmap

## Project Structure

```text
Car-Dataset-EDA/
│
├── Exploratory Data Analysis of Car Dataset.ipynb
├── Cars_data.csv
└── README.md
