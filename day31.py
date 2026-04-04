import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold, cross_val_score
def main():
    print("\n" + "=" * 70)
    print("K-FOLD CROSS VALIDATION")
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
    model = DecisionTreeClassifier(max_depth=5)
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kfold, scoring='accuracy')
    print("\nCross-Validation Scores (each fold):")
    print(scores)
    print(f"\nMean Accuracy: {scores.mean():.2f}")
    print(f"Standard Deviation: {scores.std():.2f}")
if __name__ == "__main__":
    main()