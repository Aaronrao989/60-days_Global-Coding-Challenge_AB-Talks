import pandas as pd
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df
def clean_missing_values(df):
    print("\nMissing Values Before Cleaning:")
    print(df.isnull().sum())
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    print("\nMissing Values After Cleaning:")
    print(df.isnull().sum())
    return df
def display_dataset(df):
    print("\n" + "-" * 70)
    print("CLEANED DATASET PREVIEW")
    print("-" * 70)
    print(df.head(10))
def main():
    print("\n" + "=" * 70)
    print("PANDAS DATA CLEANING SYSTEM")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        dataset = load_dataset(file_path)
        cleaned_dataset = clean_missing_values(dataset)
        display_dataset(cleaned_dataset)
    except FileNotFoundError:
        print("CSV file not found. Please check the path.")
    except Exception as e:
        print(f"Error occurred: {e}")
if __name__ == "__main__":
    main()