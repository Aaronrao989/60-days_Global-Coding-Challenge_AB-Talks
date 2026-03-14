import pandas as pd
def load_dataset(file_path):
    """Load dataset from CSV file"""
    df = pd.read_csv(file_path)
    return df
def encode_categorical_columns(df):
    """Convert categorical columns into numeric using one-hot encoding"""
    print("\nOriginal Dataset:")
    print(df.head())
    categorical_cols = df.select_dtypes(include=['object']).columns
    print("\nCategorical Columns Found:")
    print(list(categorical_cols))
    encoded_df = pd.get_dummies(df, columns=categorical_cols)
    return encoded_df
def display_dataset(df):
    print("\n" + "-" * 70)
    print("ENCODED DATASET PREVIEW")
    print("-" * 70)
    print(df.head(10))
def main():
    print("\n" + "=" * 70)
    print("PANDAS DATA TRANSFORMATION SYSTEM")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        dataset = load_dataset(file_path)
        encoded_dataset = encode_categorical_columns(dataset)
        display_dataset(encoded_dataset)
    except FileNotFoundError:
        print("⚠ CSV file not found. Please check the file path.")
    except Exception as e:
        print(f"⚠ Error occurred: {e}")
if __name__ == "__main__":
    main()