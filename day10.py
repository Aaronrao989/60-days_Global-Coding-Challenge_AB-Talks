import pandas as pd
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df
def display_preview(df):
    print("\n" + "-" * 70)
    print("DATASET PREVIEW (FIRST 10 ROWS)")
    print("-" * 70)
    print(df.head(10))
    print("\n" + "-" * 70)
    print("Dataset Loaded Successfully.")
def main():
    print("\n" + "=" * 70)
    print("PANDAS DATAFRAME DATASET INSPECTION")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        dataset = load_dataset(file_path)
        display_preview(dataset)
    except FileNotFoundError:
        print("⚠ Error: CSV file not found. Please check the file path.")
    except Exception as e:
        print(f"⚠ Unexpected error occurred: {e}")
if __name__ == "__main__":
    main()