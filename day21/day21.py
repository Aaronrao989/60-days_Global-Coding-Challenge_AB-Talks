import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def load_data(file_path):
    return pd.read_csv(file_path)
def basic_analysis(df):
    print("\n" + "-" * 70)
    print("DATASET INFORMATION")
    print("-" * 70)
    print("\nDataset Info:")
    print(df.info())

    print("\nStatistical Summary:")
    print(df.describe())

    print("\nMissing Values:")
    print(df.isnull().sum())


def statistical_analysis(df):
    print("\n" + "-" * 70)
    print("STATISTICAL ANALYSIS (CHARGES)")
    print("-" * 70)

    charges = df["charges"]

    print(f"Mean: {np.mean(charges):.2f}")
    print(f"Median: {np.median(charges):.2f}")
    print(f"Mode: {pd.Series(charges).mode().tolist()}")
    print(f"Variance: {np.var(charges):.2f}")
    print(f"Standard Deviation: {np.std(charges):.2f}")


def visualize_data(df):
    # 1. Distribution of charges
    plt.figure()
    sns.histplot(df["charges"], kde=True)
    plt.title("Distribution of Medical Charges")
    plt.xlabel("Charges")
    plt.ylabel("Frequency")
    plt.savefig("charges_distribution.png")
    plt.show()

    # 2. Age vs Charges
    plt.figure()
    sns.scatterplot(x="age", y="charges", data=df)
    plt.title("Age vs Medical Charges")
    plt.xlabel("Age")
    plt.ylabel("Charges")
    plt.savefig("age_vs_charges.png")
    plt.show()

    # 3. Smoker vs Charges
    plt.figure()
    sns.boxplot(x="smoker", y="charges", data=df)
    plt.title("Smoker vs Medical Charges")
    plt.xlabel("Smoker")
    plt.ylabel("Charges")
    plt.savefig("smoker_vs_charges.png")
    plt.show()

    # 4. Correlation Heatmap
    plt.figure()
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png")
    plt.show()


def main():
    print("\n" + "=" * 70)
    print("MINI PROJECT: EDA + STATISTICAL ANALYSIS")
    print("=" * 70)

    file_path = input("\nEnter CSV file path (e.g., train.csv): ")

    try:
        df = load_data(file_path)

        print("\nDataset Preview:")
        print(df.head())

        basic_analysis(df)
        statistical_analysis(df)
        visualize_data(df)

        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except FileNotFoundError:
        print("⚠ File not found. Please check the path.")
    except Exception as e:
        print(f"⚠ Error occurred: {e}")


if __name__ == "__main__":
    main()