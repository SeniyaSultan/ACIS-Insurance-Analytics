# Stage 4: Train Model
dvc stage add -n train_model -d src/models/train_model.py -d data/features -o models/model.pkl python src/models/train_model.py
