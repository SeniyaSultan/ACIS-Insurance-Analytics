# src/utils.py

import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def read_csv(path: str, parse_dates=None):
    logging.info(f"Loading CSV from {path}")
    return pd.read_csv(path, parse_dates=parse_dates)


def write_csv(df, path: str):
    ensure_dir(os.path.dirname(path) or ".")
    logging.info(f"Writing CSV to {path}")
    df.to_csv(path, index=False)
