import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def main():
    print("\n" + "=" * 70)
    print("FULL MACHINE LEARNING PIPELINE")
    print("=" * 70)

    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day25/customer_dataset(in).csv")

    print("\nDataset Preview:")
    print(df.head())

    drop_cols = ["Customer ID", "SKU", "Purchase Date"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

    df["Order Status"] = df["Order Status"].map({
        "Completed": 1,
        "Cancelled": 0
    })

    X = df.drop("Order Status", axis=1)
    y = df["Order Status"]

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = X.select_dtypes(include=["object"]).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", "passthrough", categorical_cols)
        ]
    )

    # Convert categorical after passthrough
    X = pd.get_dummies(X, drop_first=True)

    # Step 7: Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Step 8: Model inside pipeline
    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    # Step 9: Train
    pipeline.fit(X_train, y_train)

    # Step 10: Predict
    predictions = pipeline.predict(X_test)

    # Step 11: Evaluation
    accuracy = accuracy_score(y_test, predictions)

    print("\n" + "-" * 70)
    print("MODEL PERFORMANCE")
    print("-" * 70)
    print(f"Accuracy: {accuracy:.2f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    print("\n" + "-" * 70)
    print("PIPELINE SUMMARY")
    print("-" * 70)
    print("1. Data Loading")
    print("2. Preprocessing (encoding + scaling)")
    print("3. Model Training")
    print("4. Prediction")
    print("5. Evaluation")


if __name__ == "__main__":
    main()