import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Placeholder for Model Training Script
# As described in Section 6.2 of the prompt.

def load_historical_data():
    """
    Load data from database or CSV for training.
    """
    print("Loading historical data...")
    # Mock data
    df = pd.DataFrame({
        "humidity": [20, 80, 15, 90],
        "wind_speed": [25, 5, 30, 2],
        "temp": [40, 22, 45, 18],
        "ndvi": [0.3, 0.8, 0.2, 0.9],
        "dry_days": [30, 2, 40, 1],
        "fire": [1, 0, 1, 0] # Target variable
    })
    return df

def train_model():
    print("Starting ML Model training pipeline...")
    
    df = load_historical_data()
    X = df.drop("fire", axis=1)
    y = df["fire"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        eval_metric='logloss'
    )
    
    print("Training XGBoost Classifier...")
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the model
    os.makedirs(os.path.dirname(__file__) + '/../../ml/models', exist_ok=True)
    model_path = os.path.dirname(__file__) + '/../../ml/models/xgboost_v1.pkl'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
