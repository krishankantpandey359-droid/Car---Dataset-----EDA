# Car Dataset Exploratory Data Analysis

## Project overview

This project explores a Kaggle Cars dataset with Python, Pandas, NumPy, Matplotlib, and Seaborn. It studies vehicle attributes and their associations with manufacturer suggested retail price (MSRP). It is an exploratory data analysis project, not a deployed price-prediction model.

## Dataset

The notebook's saved outputs show an original dataset of 11,914 rows and 16 columns. The dataset includes make, model, model year, engine horsepower, cylinders, transmission, drive mode, fuel economy, and MSRP.

The notebook first checks `CARS_DATASET_PATH`, then `Cars_data.csv` in the working directory. Google Colab prompts for a CSV upload when neither is available. In local Python and CI, it downloads the public `CooperUnion/cardataset` dataset with KaggleHub and selects the CSV containing the expected columns. The raw CSV is not committed to this repository.

## Analysis workflow

1. Load and inspect the dataset and its data types.
2. Validate the expected source columns and flag suspicious non-positive values without silently deleting them.
3. Remove six columns from the current charting scope: Engine Fuel Type, Market Category, Vehicle Style, Popularity, Number of Doors, and Vehicle Size.
4. Rename Engine HP to HP, Engine Cylinders to Cylinders, Driven_Wheels to Drive Mode, and MSRP to Price.
5. Remove exact duplicate rows using a tested helper.
6. Remove rows with missing values for this exploratory analysis.
7. Review numeric distributions and potential outliers.
8. Compare vehicle counts and prices across selected categories.
9. Explore horsepower versus price and correlations among numeric variables.

## Recorded dataset counts

The following counts are from the notebook's saved outputs. Re-run the notebook with the original CSV to reproduce them.

| Stage | Rows |
|---|---:|
| Original dataset | 11,914 |
| After duplicate removal | 10,925 |
| After missing-value removal | 10,827 |
| Separate HP/Price IQR sensitivity subset | 9,191 (saved historical output) |

The IQR subset is a separate analytical view. The revised notebook calculates it using HP and Price only and preserves the cleaned `df` dataframe.

## Key findings from saved outputs

- Pearson correlation between HP and Price: approximately 0.660.
- Cylinders and Price: approximately 0.555.
- HP and Cylinders: approximately 0.788.
- Highway MPG and City MPG: approximately 0.841.
- Cylinders and City MPG: approximately -0.632.
- Cylinders and Highway MPG: approximately -0.612.

These are correlations in this dataset. They do not establish causation or represent the full car market.

## Outlier handling

The revised notebook applies the 1.5 × IQR rule to HP and Price only, then stores the filtered rows in a separate dataframe named `df2`. It does not overwrite the cleaned dataframe. Statistical outliers are review flags, not automatically invalid records. High prices and horsepower values can be valid for luxury and performance vehicles.

## Run the notebook

1. Clone or download this repository.
2. Install the packages in `requirements.txt`.
3. Optionally set `CARS_DATASET_PATH` or place `Cars_data.csv` in the working directory. Without a local file, KaggleHub downloads the public dataset in local Python/CI; Google Colab prompts for upload.
4. Run `python -m pytest -q` to check the reusable data-quality helpers.
5. Open the notebook in Jupyter or Google Colab and run all cells.

## Limitations

- The dataset is a sample of vehicle listings/specifications, not a census of all vehicles or transactions.
- Dropping missing rows can introduce bias. A modelling workflow should compare this with imputation fitted on training data only.
- Removing statistical outliers changes the population being described. Use `df` for the primary EDA and `df2` only for sensitivity comparisons.
- Correlation does not imply causation. Vehicle make, model, age, and segment can influence observed relationships.
- The notebook does not train, validate, or deploy a machine-learning model. The project includes tested helpers for schema validation, suspicious-value flags, duplicate removal and IQR sensitivity filtering. GitHub Actions installs dependencies, runs unit tests, validates notebook syntax, executes the full notebook and uploads the executed artifact.

## Project structure

```text
Car---Dataset-----EDA/
├── Exploratory Data Analysis of Car Dataset.ipynb
├── Cars_data.csv  (provide locally; not committed)
├── src/
│   └── car_eda.py
├── tests/
│   └── test_car_eda.py
├── .github/workflows/notebook-validation.yml
├── requirements.txt
└── README.md
```

## Latest GitHub Actions validation

Latest verified successful main-branch workflow run checked on 24 November 2026: [GitHub Actions run #45312045846](https://github.com/krishankantpandey359-droid/Car---Dataset-----EDA/actions/runs/45312045846). This run verifies the checks configured in this repository's workflow; it does not replace manual testing of features outside CI.
