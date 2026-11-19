from pathlib import Path
import json

import pandas as pd


NOTEBOOK = Path(__file__).parents[1] / "Exploratory Data Analysis of Car Dataset.ipynb"


def test_notebook_is_valid_and_numeric_selection_is_dtype_based():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    sources = [
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]
    numeric_cells = [source for source in sources if "numeric_df" in source]
    assert numeric_cells, "Expected a numeric-column selection cell."
    assert "select_dtypes" in numeric_cells[0]
    assert "include=" in numeric_cells[0]


def test_numeric_selection_excludes_text_columns():
    sample = pd.DataFrame({
        "Make": ["Ford", "Honda"],
        "HP": [150, 180],
        "Price": [12000.0, 18000.0],
    })
    numeric = sample.select_dtypes(include=["number"])
    assert numeric.columns.tolist() == ["HP", "Price"]
    assert numeric.shape == (2, 2)
