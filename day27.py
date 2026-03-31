import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix
)
def main():
    print("\n" + "=" * 70)
    print("MODEL EVALUATION USING REAL DATASET")
    print("=" * 70)

    # Step 1: Load dataset
    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day26/customer_dataset(in).csv")

    print("\nDataset Preview:")
    print(df.head())

    # Step 2: Drop unnecessary columns
    df = df.drop(["Customer ID", "SKU", "Purchase Date"], axis=1)

    # Step 3: Convert target to numeric
    df["Order Status"] = df["Order Status"].map({
        "Completed": 1,
        "Cancelled": 0
    })

    # Step 4: Encode categorical variables
    df = pd.get_dummies(df, drop_first=True)

    # Step 5: Features & Target
    X = df.drop("Order Status", axis=1)
    y = df["Order Status"]

    # Step 6: Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Step 7: Train model
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_train, y_train)

    # Step 8: Predictions
    predictions = model.predict(X_test)

    print("\nSample Predictions vs Actual:")
    for i in range(min(5, len(predictions))):
        print(f"Predicted: {predictions[i]} | Actual: {y_test.iloc[i]}")

    # Step 9: Evaluation Metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)

    print("\n" + "-" * 70)
    print("EVALUATION METRICS")
    print("-" * 70)
    print(f"Accuracy : {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall   : {recall:.2f}")

    # Step 10: Confusion Matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    # Step 11: Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    main()