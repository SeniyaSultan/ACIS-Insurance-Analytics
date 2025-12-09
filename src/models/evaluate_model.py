
# Stage 5: Evaluate Model
dvc stage add -n evaluate_model -d src/models/evaluate_model.py -d models/model.pkl -o reports/metrics.json python src/models/evaluate_model.py
