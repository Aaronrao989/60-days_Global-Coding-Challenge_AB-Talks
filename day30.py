import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
def main():
    print("\n" + "=" * 70)
    print("FEATURE SCALING: STANDARDIZATION & NORMALIZATION")
    print("=" * 70)
    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day25/customer_dataset(in).csv")
    print("\nOriginal Dataset:")
    print(df.head())
    drop_cols = ["Customer ID", "SKU", "Purchase Date"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    if "Order Status" in df.columns:
        df["Order Status"] = df["Order Status"].map({
            "Completed": 1,
            "Cancelled": 0
        })
    df_encoded = pd.get_dummies(df, drop_first=True)
    X = df_encoded.drop("Order Status", axis=1)
    print("\nBefore Scaling:")
    print(X.head())
    standard_scaler = StandardScaler()
    X_standardized = standard_scaler.fit_transform(X)
    X_standardized_df = pd.DataFrame(X_standardized, columns=X.columns)
    print("\nAfter Standardization (Mean ~ 0, Std ~ 1):")
    print(X_standardized_df.head())
    minmax_scaler = MinMaxScaler()
    X_normalized = minmax_scaler.fit_transform(X)
    X_normalized_df = pd.DataFrame(X_normalized, columns=X.columns)
    print("\nAfter Normalization (Range 0 to 1):")
    print(X_normalized_df.head())
if __name__ == "__main__":
    main()