# README.md (starter)

# Insurance Risk Analytics — Starter Repo

This repo contains a lightweight starter codebase for the End-to-End Insurance Risk Analytics challenge.

## Quickstart

1. Create a Python virtual environment and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Add your raw CSV to `data/raw/insurance_data.csv`

3. Initialize DVC (if not already):

```bash
dvc init
dvc remote add -d localremote ./data_storage
dvc add data/raw/insurance_data.csv
git add data/raw/insurance_data.csv.dvc .gitignore
git commit -m "track raw data with dvc"
```

4. Run preprocessing:

```bash
python src/data_preprocessing.py --input data/raw/insurance_data.csv --output data/processed/cleaned.csv
```

5. Run EDA:

```bash
python src/eda.py --input data/processed/cleaned.csv --outdir reports/figures
```

6. Run hypothesis tests:

```bash
python src/hypothesis_tests.py --input data/processed/cleaned.csv
```

7. Train models:

```bash
python src/models.py --input data/processed/cleaned.csv --outdir models/
```

---

## Notes

- Fill in TODOs in scripts to match your dataset column names and business logic.
- Keep notebooks for exploration only; move production code to `src/`.
- Use branches: `task-1`, `task-2`, `task-3`, `task-4`. Merge via PRs.
