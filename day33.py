import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
def main():
    print("\n" + "=" * 70)
    print("ENSEMBLE LEARNING: DECISION TREE vs RANDOM FOREST")
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
    df_encoded = pd.get_dummies(df, drop_first=True)
    X = df_encoded.drop("Order Status", axis=1)
    y = df_encoded["Order Status"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    dt_model = DecisionTreeClassifier(max_depth=5)
    dt_model.fit(X_train, y_train)
    dt_predictions = dt_model.predict(X_test)
    dt_accuracy = accuracy_score(y_test, dt_predictions)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_predictions)
    print("\n" + "-" * 70)
    print("MODEL COMPARISON")
    print("-" * 70)
    print(f"Decision Tree Accuracy : {dt_accuracy:.2f}")
    print(f"Random Forest Accuracy: {rf_accuracy:.2f}")
    print("\n" + "-" * 70)
    print("RANDOM FOREST DETAILED REPORT")
    print("-" * 70)
    print(classification_report(y_test, rf_predictions))
    print("\n" + "-" * 70)
    print("INSIGHT")
    print("-" * 70)
    if rf_accuracy > dt_accuracy:
        print("Random Forest performed better due to ensemble learning.")
    else:
        print("Performance is similar, dataset may be simple or small.")
    print("\nRandom Forest reduces overfitting by combining multiple trees.")
if __name__ == "__main__":
    main()