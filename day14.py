import pandas as pd
def load_dataset(file_path):
    """Load dataset from CSV file"""
    df = pd.read_csv(file_path)
    return df
def clean_dataset(df):
    print("\nInitial Dataset Info:")
    print(df.info())
    print("\nMissing Values Before Cleaning:")
    print(df.isnull().sum())
    df = df.drop_duplicates()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    numeric_cols = df.select_dtypes(include="number").columns
    df.loc[:, numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        df.loc[:, col] = df[col].fillna(df[col].mode()[0])
    print("\nMissing Values After Cleaning:")
    print(df.isnull().sum())
    return df
def display_preview(df):
    print("\n" + "-" * 70)
    print("CLEANED DATASET PREVIEW")
    print("-" * 70)
    print(df.head(10))
def main():
    print("\n" + "=" * 70)
    print("PANDAS DATA CLEANING & PREPROCESSING SYSTEM")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        dataset = load_dataset(file_path)
        print("\nDataset Preview:")
        print(dataset.head())
        cleaned_dataset = clean_dataset(dataset)
        display_preview(cleaned_dataset)
    except FileNotFoundError:
        print("CSV file not found. Please check the file path.")
    except Exception as e:
        print(f"Error occurred: {e}")
if __name__ == "__main__":
    main()