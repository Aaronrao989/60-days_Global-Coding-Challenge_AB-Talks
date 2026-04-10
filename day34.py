import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report


def main():
    print("\n" + "=" * 70)
    print("ADVANCED ENSEMBLE COMPARISON: RANDOM FOREST vs GRADIENT BOOSTING")
    print("=" * 70)

    df = pd.read_csv("day25/customer_dataset(in).csv")

    print("\nDataset Preview:")
    print(df.head())

    drop_cols = ["Customer ID", "SKU", "Purchase Date"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])

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

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    rf_train_pred = rf.predict(X_train)
    rf_test_pred = rf.predict(X_test)

    rf_train_acc = accuracy_score(y_train, rf_train_pred)
    rf_test_acc = accuracy_score(y_test, rf_test_pred)

    gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    gb.fit(X_train, y_train)

    gb_train_pred = gb.predict(X_train)
    gb_test_pred = gb.predict(X_test)

    gb_train_acc = accuracy_score(y_train, gb_train_pred)
    gb_test_acc = accuracy_score(y_test, gb_test_pred)

    print("\n" + "-" * 70)
    print("MODEL PERFORMANCE (Train vs Test)")
    print("-" * 70)

    print(f"Random Forest → Train: {rf_train_acc:.2f} | Test: {rf_test_acc:.2f}")
    print(f"Gradient Boost → Train: {gb_train_acc:.2f} | Test: {gb_test_acc:.2f}")

    print("\n" + "-" * 70)
    print("OVERFITTING ANALYSIS")
    print("-" * 70)

    print(f"Random Forest Gap: {round(rf_train_acc - rf_test_acc, 2)}")
    print(f"Gradient Boost Gap: {round(gb_train_acc - gb_test_acc, 2)}")

    print("\n" + "-" * 70)
    print("CLASSIFICATION REPORT (Gradient Boosting)")
    print("-" * 70)
    print(classification_report(y_test, gb_test_pred))

    print("\n" + "-" * 70)
    print("FEATURE IMPORTANCE (Random Forest)")
    print("-" * 70)

    importance = pd.Series(rf.feature_importances_, index=X.columns)
    print(importance.sort_values(ascending=False))

    print("\n" + "-" * 70)
    print("FINAL INSIGHT")
    print("-" * 70)

    if gb_test_acc > rf_test_acc:
        print("Gradient Boosting performs better → learns from mistakes (reduces bias).")
    else:
        print("Random Forest performs better → more stable and reduces variance.")

    print("\nKey Difference:")
    print("Random Forest → Bagging (parallel learning)")
    print("Gradient Boosting → Sequential learning")


if __name__ == "__main__":
    main()