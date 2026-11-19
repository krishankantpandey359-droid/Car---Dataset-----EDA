import numpy as np
import pandas as pd
import pytest

from src.car_eda import (
    data_quality_flags,
    iqr_sensitivity_filter,
    remove_exact_duplicates,
    validate_cars,
)


@pytest.fixture
def cars():
    return pd.DataFrame({
        "Make": ["Ford", "Honda", "Toyota", "Ford", "BMW"],
        "Model": ["A", "B", "C", "A", "D"],
        "Year": [2020, 2019, 2018, 2020, 2017],
        "Engine HP": [150, 130, 170, 150, 300],
        "Engine Cylinders": [4, 4, 6, 4, 8],
        "highway MPG": [30, 35, 28, 30, 22],
        "city mpg": [22, 27, 20, 22, 15],
        "MSRP": [20000, 18000, 25000, 20000, 90000],
        "extra": [1, 2, 3, 1, 5],
    })


def test_validate_cars_rejects_missing_required_columns(cars):
    with pytest.raises(ValueError, match="Model"):
        validate_cars(cars.drop(columns=["Model"]))


def test_validate_cars_rejects_empty_data(cars):
    with pytest.raises(ValueError, match="empty"):
        validate_cars(cars.iloc[:0])


def test_quality_flags_separate_missing_invalid_and_non_positive(cars):
    cars.loc[0, "Year"] = 0
    cars.loc[1, "MSRP"] = -10
    cars["Engine HP"] = cars["Engine HP"].astype(object)
    cars.loc[2, "Engine HP"] = "not recorded"
    cars.loc[3, "highway MPG"] = np.nan
    flags = data_quality_flags(cars)
    assert flags.loc["Year", "non_positive_year"] == 1
    assert flags.loc["MSRP", "non_positive_msrp"] == 1
    assert flags.loc["Engine HP", "non_numeric_or_non_finite"] == 1
    assert flags.loc["highway MPG", "missing_values"] == 1


def test_remove_exact_duplicates_returns_copy(cars):
    duplicated = pd.concat([cars, cars.iloc[[0]]], ignore_index=True)
    cleaned = remove_exact_duplicates(duplicated)
    assert len(cleaned) == len(cars) - 1
    assert len(duplicated) == len(cars) + 1


def test_iqr_filter_keeps_original_and_flags_extreme_value():
    frame = pd.DataFrame({
        "HP": [100, 110, 120, 130, 140, 1000],
        "Price": [10000, 11000, 12000, 13000, 14000, 90000],
    })
    filtered, mask = iqr_sensitivity_filter(frame)
    assert mask.sum() == 1 and len(filtered) == 5 and len(frame) == 6


def test_iqr_filter_rejects_missing_columns(cars):
    with pytest.raises(ValueError, match="Missing IQR columns"):
        iqr_sensitivity_filter(cars, columns=("not_a_column",))


def test_iqr_filter_rejects_invalid_multiplier(cars):
    with pytest.raises(ValueError, match="finite positive"):
        iqr_sensitivity_filter(cars, multiplier=float("inf"))


def test_iqr_filter_rejects_invalid_numeric_values():
    frame = pd.DataFrame({"HP": [100, 110, np.nan], "Price": [10000, 11000, 12000]})
    with pytest.raises(ValueError, match="finite numeric"):
        iqr_sensitivity_filter(frame)

@pytest.mark.parametrize("multiplier", [True, False, "1.5", None])
def test_iqr_filter_rejects_boolean_and_non_numeric_multiplier(cars, multiplier):
    with pytest.raises(ValueError, match="boolean or non-numeric"):
        iqr_sensitivity_filter(cars, multiplier=multiplier)




def test_validate_cars_rejects_duplicate_column_names(cars):
    cars.columns = list(cars.columns[:-1]) + ["Make"]
    with pytest.raises(ValueError, match="duplicate column names"):
        validate_cars(cars)


def test_data_quality_flags_do_not_mutate_input(cars):
    original = cars.copy(deep=True)
    data_quality_flags(cars)
    pd.testing.assert_frame_equal(cars, original)
