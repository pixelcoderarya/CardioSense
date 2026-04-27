import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import warnings

warnings.filterwarnings('ignore')

def main():
    print("Starting ML Pipeline...")
    
    # 1. Load Data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data')
    files = ['heart_a.csv', 'heart_b.csv', 'feature_c.csv', 'feature_d.csv', 'feature_e.csv', 'feature_f.csv']
    dfs = []

    for file in files:
        file_path = os.path.join(data_path, file)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            print(f"Warning: {file} not found in {data_path}")

    if not dfs:
        raise FileNotFoundError("No acoustic data files found in the data directory!")

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"Total rows before deduplication: {len(df_all)}")
    df_all = df_all.drop_duplicates()
    print(f"Total rows after deduplication: {len(df_all)}")

    # 2. Handle Class Imbalance (Undersample to 2:1 ratio)
    df_normal = df_all[df_all['label'] == 0]
    df_abnormal = df_all[df_all['label'] == 1]

    print(f"Original Class Balance - Normal: {len(df_normal)}, Abnormal: {len(df_abnormal)}")

    # Undersample normal class to be exactly twice the size of abnormal class
    target_normal_size = len(df_abnormal) * 2

    if len(df_normal) > target_normal_size:
        df_normal = df_normal.sample(n=target_normal_size, random_state=42)

    df_balanced = pd.concat([df_normal, df_abnormal]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Balanced Class Balance - Normal: {len(df_balanced[df_balanced['label'] == 0])}, Abnormal: {len(df_balanced[df_balanced['label'] == 1])}")

    # 3. Prepare Features and Target
    X = df_balanced.drop(columns=['label'])
    y = df_balanced['label']

    # Ensure models directory exists
    models_dir = os.path.join(current_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    # Save Feature Stats for UI Validation
    feature_stats = {}
    for col in X.columns:
        feature_stats[col] = {
            'min': float(X[col].min()),
            'max': float(X[col].max()),
            'mean': float(X[col].mean())
        }

    with open(os.path.join(models_dir, 'feature_stats.json'), 'w') as f:
        json.dump(feature_stats, f, indent=4)
    print("Saved feature_stats.json")

    # 4. Train-Test Split & Scaling
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    print("Saved scaler.pkl")

    # 5. Train Models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, class_weight='balanced', random_state=42),
        'XGBoost': XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05, scale_pos_weight=2, random_state=42),
        'LightGBM': LGBMClassifier(n_estimators=300, num_leaves=63, learning_rate=0.05, class_weight='balanced', random_state=42, verbose=-1)
    }

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        
        print(f"{name} - Accuracy: {acc:.4f}, AUC: {auc:.4f}")
        
        # Save Model
        filename = name.lower().replace(' ', '_') + '_model.pkl'
        joblib.dump(model, os.path.join(models_dir, filename))

    print("\n--- Training Complete! ---")
    print("All models, scaler, and feature_stats.json have been saved to the ml/models/ directory.")

if __name__ == "__main__":
    main()
