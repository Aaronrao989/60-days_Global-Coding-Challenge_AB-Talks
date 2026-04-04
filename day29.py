import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def main():
    print("\n" + "=" * 70)
    print("FEATURE SELECTION USING CORRELATION (CSV DATASET)")
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
    corr_matrix = df_encoded.corr()
    target_corr = corr_matrix["Order Status"].sort_values(ascending=False)
    print("\nCorrelation with Target (Order Status):")
    print(target_corr)
    plt.figure(figsize=(12, 7))
    sns.heatmap(corr_matrix, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()
    threshold = 0.2
    important_features = target_corr[abs(target_corr) > threshold].index.tolist()
    important_features = [f for f in important_features if f != "Order Status"]
    print("\nImportant Features (|correlation| >", threshold, "):")
    print(important_features)
if __name__ == "__main__":
    main()