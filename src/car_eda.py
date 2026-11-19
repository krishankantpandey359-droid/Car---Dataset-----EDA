"""Reusable data-quality and outlier helpers for the Cars EDA project."""
from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"Make", "Model", "Year", "Engine HP", "MSRP"}
QUALITY_COLUMNS = {
    "Year": "non_positive_year",
    "Engine HP": "non_positive_horsepower",
    "Engine Cylinders": "non_positive_cylinders",
    "highway MPG": "non_positive_highway_mpg",
    "city mpg": "non_positive_city_mpg",
    "MSRP": "non_positive_msrp",
}


def validate_cars(frame: pd.DataFrame) -> None:
    """Validate the minimum schema required for the car dataset."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("Cars dataset is empty.")
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Cars dataset is missing required columns: {sorted(missing)}")


def data_quality_flags(frame: pd.DataFrame) -> pd.DataFrame:
    """Count missing, non-numeric, non-finite and non-positive values per field.

    Non-positive counts apply only to values successfully parsed as finite
    numbers. Invalid/missing values are reported separately, never silently
    treated as valid measurements.
    """
    validate_cars(frame)
    records = []
    for column, non_positive_label in QUALITY_COLUMNS.items():
        if column not in frame.columns:
            continue
        raw = frame[column]
        numeric = pd.to_numeric(raw, errors="coerce")
        finite = pd.Series(np.isfinite(numeric.to_numpy(dtype=float, na_value=np.nan)),
                           index=frame.index)
        invalid = numeric.isna() | ~finite
        records.append({
            "column": column,
            "missing_values": int(raw.isna().sum()),
            "non_numeric_or_non_finite": int(invalid.sum()),
            non_positive_label: int((finite & numeric.le(0)).sum()),
            "valid_positive_values": int((finite & numeric.gt(0)).sum()),
        })
    return pd.DataFrame(records).set_index("column") if records else pd.DataFrame()


def remove_exact_duplicates(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows from a prepared analysis dataframe."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("Cannot deduplicate an empty dataframe.")
    return frame.drop_duplicates().copy()


def iqr_sensitivity_filter(
    frame: pd.DataFrame,
    columns: tuple[str, ...] = ("HP", "Price"),
    multiplier: float = 1.5,
) -> tuple[pd.DataFrame, pd.Series]:
    """Return an IQR-filtered copy and row mask; original data stays unchanged."""
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")
    if frame.empty:
        raise ValueError("Cannot calculate IQR on an empty dataframe.")
    if isinstance(multiplier, (bool, np.bool_)) or not isinstance(multiplier, (int, float, np.integer, np.floating)) or not np.isfinite(multiplier) or multiplier <= 0:
        raise ValueError("IQR multiplier must be a finite positive number, not a boolean or non-numeric value.")
    if not columns:
        raise ValueError("At least one IQR column is required.")
    missing = set(columns).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing IQR columns: {sorted(missing)}")
    numeric = frame.loc[:, list(columns)].apply(pd.to_numeric, errors="coerce")
    if not np.isfinite(numeric.to_numpy(dtype=float, na_value=np.nan)).all():
        raise ValueError("IQR columns must contain only finite numeric values.")
    q1, q3 = numeric.quantile(.25), numeric.quantile(.75)
    spread = q3 - q1
    mask = ((numeric < q1 - multiplier * spread) |
            (numeric > q3 + multiplier * spread)).any(axis=1)
    return frame.loc[~mask].copy(), mask
