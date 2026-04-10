import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def main():
    print("\n" + "=" * 70)
    print("CUSTOMER SEGMENTATION USING KMEANS (CSV DATASET)")
    print("=" * 70)

    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day25/customer_dataset(in).csv")

    print("\nDataset Preview:")
    print(df.head())

    features = ["Age", "Total Price", "Quantity"]

    features = [col for col in features if col in df.columns]

    if len(features) < 2:
        print("❌ Not enough valid numerical columns found for clustering.")
        return

    X = df[features]

    X = X.fillna(X.mean())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X_scaled)

    print("\nCluster Assignment:")
    print(df[features + ["Cluster"]].head())

    print("\nCluster Summary (Mean Values):")
    print(df.groupby("Cluster")[features].mean())

    if len(features) >= 2:
        plt.scatter(df[features[0]], df[features[1]], c=df["Cluster"])
        plt.xlabel(features[0])
        plt.ylabel(features[1])
        plt.title("Customer Segmentation (KMeans)")
        plt.show()

    print("\nClustering completed successfully ✅")

if __name__ == "__main__":
    main()