import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
def main():
    print("\n" + "=" * 70)
    print("BIAS-VARIANCE ANALYSIS (UNDERFITTING vs OVERFITTING)")
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
    underfit_model = DecisionTreeClassifier(max_depth=1)  # too simple
    underfit_model.fit(X_train, y_train)

    train_pred_under = underfit_model.predict(X_train)
    test_pred_under = underfit_model.predict(X_test)

    train_acc_under = accuracy_score(y_train, train_pred_under)
    test_acc_under = accuracy_score(y_test, test_pred_under)
    overfit_model = DecisionTreeClassifier(max_depth=None)  # too complex
    overfit_model.fit(X_train, y_train)

    train_pred_over = overfit_model.predict(X_train)
    test_pred_over = overfit_model.predict(X_test)

    train_acc_over = accuracy_score(y_train, train_pred_over)
    test_acc_over = accuracy_score(y_test, test_pred_over)

    print("\n" + "-" * 70)
    print("UNDERFITTING MODEL (High Bias)")
    print("-" * 70)
    print(f"Training Accuracy: {train_acc_under:.2f}")
    print(f"Testing Accuracy : {test_acc_under:.2f}")

    print("\n" + "-" * 70)
    print("OVERFITTING MODEL (High Variance)")
    print("-" * 70)
    print(f"Training Accuracy: {train_acc_over:.2f}")
    print(f"Testing Accuracy : {test_acc_over:.2f}")

    print("\n" + "-" * 70)
    print("INTERPRETATION")
    print("-" * 70)
    print("• Underfitting → Low training & testing accuracy")
    print("• Overfitting → High training accuracy, lower testing accuracy")
    print("• Goal → Balance both for best generalization")


if __name__ == "__main__":
    main()