# src/eda.py

"""
Exploratory Data Analysis script
Usage:
python src/eda.py --input data/processed/cleaned.csv --outdir reports/figures
Produces:

* Loss ratio by province bar chart
* TotalClaims distribution histogram
* Monthly claims trend timeseries
"""

import argparse
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.utils import read_csv, ensure_dir, logging


def plot_loss_ratio_by_province(df: pd.DataFrame, outpath: str):
    if "Province" not in df.columns or "loss_ratio" not in df.columns:
        logging.warning("Province or loss_ratio missing; skipping plot")
        return
    agg = df.groupby("Province", dropna=False).agg(
        loss_ratio=("loss_ratio", "mean"), n=("loss_ratio", "count")
    ).reset_index()
    agg = agg.sort_values("loss_ratio", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x="loss_ratio", y="Province", data=agg)
    plt.xlabel("Average Loss Ratio (TotalClaims / TotalPremium)")
    plt.title("Loss Ratio by Province")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    logging.info(f"Saved plot to {outpath}")


def plot_totalclaims_distribution(df: pd.DataFrame, outpath: str):
    if "TotalClaims" not in df.columns:
        logging.warning("TotalClaims missing; skipping plot")
        return
    plt.figure(figsize=(8, 5))
    sns.histplot(df["TotalClaims"].dropna(), bins=80, log_scale=(True, False))
    plt.xlabel("TotalClaims (log scale on x)")
    plt.title("Distribution of TotalClaims")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    logging.info(f"Saved plot to {outpath}")


def plot_monthly_claims_trend(df: pd.DataFrame, outpath: str):
    if "TransactionMonth" not in df.columns or "TotalClaims" not in df.columns:
        logging.warning("TransactionMonth or TotalClaims missing; skipping plot")
        return
    df["TransactionMonth"] = pd.to_datetime(df["TransactionMonth"], errors="coerce")
    monthly = df.set_index("TransactionMonth").resample("M")["TotalClaims"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(x="TransactionMonth", y="TotalClaims", data=monthly, marker="o")
    plt.title("Monthly Total Claims")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    logging.info(f"Saved plot to {outpath}")


def main(input_path: str, outdir: str):
    ensure_dir(outdir)
    df = read_csv(input_path, parse_dates=["TransactionMonth"])
    plot_loss_ratio_by_province(df, os.path.join(outdir, "loss_ratio_by_province.png"))
    plot_totalclaims_distribution(df, os.path.join(outdir, "totalclaims_distribution.png"))
    plot_monthly_claims_trend(df, os.path.join(outdir, "monthly_claims_trend.png"))
    logging.info("EDA done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    main(args.input, args.outdir)
