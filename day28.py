import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
def main():
    print("\n" + "=" * 70)
    print("END-TO-END ML CLASSIFICATION PIPELINE")
    print("=" * 70)
    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day26/customer_dataset(in).csv")
    print("\nDataset Preview:")
    print(df.head())
    df = df.drop(["Customer ID", "SKU", "Purchase Date"], axis=1)
    df["Order Status"] = df["Order Status"].map({
        "Completed": 1,
        "Cancelled": 0
    })
    df = pd.get_dummies(df, drop_first=True)
    X = df.drop("Order Status", axis=1)
    y = df["Order Status"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print("\nSample Predictions vs Actual:")
    for i in range(min(5, len(predictions))):
        print(f"Predicted: {predictions[i]} | Actual: {y_test.iloc[i]}")
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    print("\n" + "-" * 70)
    print("MODEL PERFORMANCE")
    print("-" * 70)
    print(f"Accuracy : {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall   : {recall:.2f}")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))
if __name__ == "__main__":
    main()