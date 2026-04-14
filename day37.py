import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def main():
    print("\n" + "=" * 70)
    print("DIMENSIONALITY REDUCTION USING PCA")
    print("=" * 70)

    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day26/customer_dataset(in).csv")

    print("\nDataset Preview:")
    print(df.head())

    drop_cols = ["Customer ID", "SKU", "Purchase Date"]
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    numeric_df = df.select_dtypes(include=["int64", "float64"])

    if numeric_df.shape[1] < 2:
        print("❌ Not enough numerical features for PCA.")
        return

    print("\nUsing Numerical Features:")
    print(numeric_df.columns.tolist())

    numeric_df = numeric_df.fillna(numeric_df.mean())
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_data)

    pca_df = pd.DataFrame(
        data=principal_components,
        columns=["PC1", "PC2"]
    )

    print("\nExplained Variance Ratio:")
    print(pca.explained_variance_ratio_)

    plt.scatter(pca_df["PC1"], pca_df["PC2"])
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA Visualization (2D Projection)")
    plt.show()

    print("\nPCA successfully reduced dimensions")

if __name__ == "__main__":
    main()