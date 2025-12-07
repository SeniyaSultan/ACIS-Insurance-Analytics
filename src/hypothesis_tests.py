# src/hypothesis_tests.py

"""
Hypothesis testing utilities
Usage example:
python src/hypothesis_tests.py --input data/processed/cleaned.csv
"""

import argparse
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from src.utils import read_csv, logging

def anova_test(df, group_col, value_col):
groups = [g.dropna() for _, g in df.groupby(group_col)[value_col]]
f, p = stats.f_oneway(*groups)
return f, p

def chi2_test_frequency(df, group_col, event_col):
# event_col should be binary: 1 if claim occurred, 0 otherwise
contingency = pd.crosstab(df[group_col], df[event_col])
chi2, p, dof, expected = stats.chi2_contingency(contingency)
return chi2, p, dof

def compare_two_groups_ttest(df, group_col, value_col, groupA, groupB):
a = df[df[group_col] == groupA][value_col].dropna()
b = df[df[group_col] == groupB][value_col].dropna()
t, p = stats.ttest_ind(a, b, equal_var=False)
return t, p

def run_all_tests(df):
results = {}
# H0: no risk differences across provinces -> test loss_ratio by province
if "Province" in df.columns and "loss_ratio" in df.columns:
f, p = anova_test(df, "Province", "loss_ratio")
results["province_anova"] = {"f": f, "p": p}
logging.info(f"Province ANOVA p-value: {p:.4f}")
# If significant, run Tukey HSD
if p < 0.05:
tukey = pairwise_tukeyhsd(df["loss_ratio"].dropna(), df["Province"].loc[df["loss_ratio"].notna()])
logging.info(str(tukey.summary()))
# H0: risk differences between zipcodes -> you may want to sample top N zipcodes
# H0: margin differences and gender differences
return results

def main(input_path: str):
df = read_csv(input_path)
# Create a binary claim indicator if not present
if "TotalClaims" in df.columns:
df["has_claim"] = df["TotalClaims"].fillna(0) > 0
results = run_all_tests(df)
print("Test results:", results)

if **name** == "**main**":
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()
main(args.input)
