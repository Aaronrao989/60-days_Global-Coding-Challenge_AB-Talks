import pandas as pd
def extract_data():
    print("Extracting data...")
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David", None],
        "Age": [25, 30, None, 40, 35],
        "Salary": [50000, 60000, 70000, None, 80000]
    }
    df = pd.DataFrame(data)
    return df
def transform_data(df):
    print("Transforming data...")
    df["Name"].fillna("Unknown", inplace=True)
    df["Age"].fillna(df["Age"].mean(), inplace=True)
    df["Salary"].fillna(df["Salary"].mean(), inplace=True)
    df["Salary_After_Tax"] = df["Salary"] * 0.9
    return df
def load_data(df):
    print("Loading data...")
    df.to_csv("processed_data.csv", index=False)
    print("Data saved successfully!")
def run_pipeline():
    df = extract_data()
    print("\nRaw Data:\n", df)
    df = transform_data(df)
    print("\nProcessed Data:\n", df)
    load_data(df)
if __name__ == "__main__":
    run_pipeline()