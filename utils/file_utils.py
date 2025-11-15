# utils/file_utils.py
"""
File and Data Utilities for Yojanasaathi
Handles data loading for CSV and JSON files.
"""

import pandas as pd
import os

def load_csv(path):
    """
    Loads a CSV file at `path` into a pandas DataFrame.
    Returns:
        pd.DataFrame: Loaded data or empty DataFrame if load fails.
    """
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def load_json(path):
    """
    Loads a JSON file at `path`.
    Returns:
        object: Loaded Python object or None on failure.
    """
    import json
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

# End of utils/file_utils.py
