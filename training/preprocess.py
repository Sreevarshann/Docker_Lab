import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def load_data(path: str):
    """Load the diabetes dataset from a CSV file."""
    print(f"📄 Reading dataset from: {path}")
    return pd.read_csv(path)

def build_preprocess_pipeline():
    """Create a simple preprocessing pipeline."""
    pipeline = Pipeline([
        ("scaler", StandardScaler())
    ])
    return pipeline
