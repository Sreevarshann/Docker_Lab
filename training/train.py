import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from preprocess import load_data, build_preprocess_pipeline
import time

# Inside Docker container, dataset path is:
DATA_PATH = "/app/data/diabetes.csv"

# Model output paths (saved on mounted volume)
MODEL_PATH = "/app/model/model.pkl"
PREPROCESSOR_PATH = "/app/model/preprocess.pkl"


def main():
    print("📥 Loading dataset...")
    df = load_data(DATA_PATH)

    print("🔧 Splitting features and target...")
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    print("🔨 Building preprocessing pipeline...")
    preprocessor = build_preprocess_pipeline()

    print("⚙️ Preprocessing data...")
    X_processed = preprocessor.fit_transform(X)

    print("✂️ Train-test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    print("🤖 Training model (Logistic Regression)...")
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    print("💾 Saving trained model...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("💾 Saving preprocessor...")
    with open(PREPROCESSOR_PATH, "wb") as f:
        pickle.dump(preprocessor, f)

    print("✅ Training complete! Model saved.")

    # ---------------------------------------------------------------------
    # 🔒 IMPORTANT: Keep training container alive so healthcheck works
    # ---------------------------------------------------------------------
    print("⏳ Training container is now idle and waiting (for healthcheck)...")
    while True:
        time.sleep(3600)  # Sleep 1 hour repeatedly (container stays alive)


if __name__ == "__main__":
    main()
