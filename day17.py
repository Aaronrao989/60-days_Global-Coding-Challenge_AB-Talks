import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df
def basic_info(df):
    print("\nDataset Info:")
    print(df.info())
    print("\nStatistical Summary:")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())
def visualize_data(df):
    plt.figure(figsize=(10, 5))
    sns.histplot(df["charges"], kde=True)
    plt.title("Distribution of Insurance Charges")
    plt.savefig("charges_distribution.png")
    plt.show()
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="age", y="charges", data=df)
    plt.title("Age vs Charges")
    plt.savefig("age_vs_charges.png")
    plt.show()
    plt.figure(figsize=(6, 5))
    sns.boxplot(x="smoker", y="charges", data=df)
    plt.title("Charges by Smoking Status")
    plt.savefig("smoker_vs_charges.png")
    plt.show()
def main():
    print("\n" + "=" * 70)
    print("EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    df = load_data(file_path)
    print("\nDataset Preview:")
    print(df.head())
    basic_info(df)
    visualize_data(df)
if __name__ == "__main__":
    main()