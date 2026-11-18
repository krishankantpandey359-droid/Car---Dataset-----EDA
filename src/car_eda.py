"""Reusable data-quality and outlier helpers for the Cars EDA project."""
from __future__ import annotations
import pandas as pd
REQUIRED_COLUMNS = {"Make", "Model", "Year", "Engine HP", "MSRP"}
QUALITY_COLUMNS = {"Year":"non_positive_year","Engine HP":"non_positive_horsepower","Engine Cylinders":"non_positive_cylinders","highway MPG":"non_positive_highway_mpg","city mpg":"non_positive_city_mpg","MSRP":"non_positive_msrp"}
def validate_cars(frame: pd.DataFrame) -> None:
    if not isinstance(frame,pd.DataFrame): raise TypeError("Expected a pandas DataFrame.")
    if frame.empty: raise ValueError("Cars dataset is empty.")
    missing=REQUIRED_COLUMNS.difference(frame.columns)
    if missing: raise ValueError(f"Cars dataset is missing required columns: {sorted(missing)}")
def data_quality_flags(frame: pd.DataFrame) -> pd.Series:
    validate_cars(frame); flags={}
    for column,label in QUALITY_COLUMNS.items():
        if column in frame.columns: flags[label]=int((pd.to_numeric(frame[column],errors="coerce")<=0).sum())
    return pd.Series(flags,name="row_count",dtype="int64")
def remove_exact_duplicates(frame: pd.DataFrame) -> pd.DataFrame:
    validate_cars(frame); return frame.drop_duplicates().copy()
def iqr_sensitivity_filter(frame: pd.DataFrame, columns: tuple[str,...]=("HP","Price"), multiplier: float=1.5) -> tuple[pd.DataFrame,pd.Series]:
    if not isinstance(frame,pd.DataFrame): raise TypeError("Expected a pandas DataFrame.")
    if frame.empty: raise ValueError("Cannot calculate IQR on an empty dataframe.")
    if multiplier<=0: raise ValueError("IQR multiplier must be positive.")
    if not columns: raise ValueError("At least one IQR column is required.")
    missing=set(columns).difference(frame.columns)
    if missing: raise ValueError(f"Missing IQR columns: {sorted(missing)}")
    numeric=frame.loc[:,list(columns)].apply(pd.to_numeric,errors="coerce")
    q1,q3=numeric.quantile(.25),numeric.quantile(.75); spread=q3-q1
    mask=((numeric<q1-multiplier*spread)|(numeric>q3+multiplier*spread)).any(axis=1)
    return frame.loc[~mask].copy(),mask
