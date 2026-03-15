import pandas as pd
def load_dataset(file_path):
    """Load dataset from CSV file"""
    df = pd.read_csv(file_path)
    return df
def analyze_sales_by_region(df):
    """Group sales by region and calculate total sales"""
    grouped_sales = df.groupby("Region")["Sales"].sum()
    return grouped_sales
def display_results(grouped_sales):
    print("\n" + "-" * 70)
    print("TOTAL SALES BY REGION")
    print("-" * 70)
    print(grouped_sales)
    print("\n" + "-" * 70)
    print("Sales Analysis Completed Successfully.")
def main():
    print("\n" + "=" * 70)
    print("PANDAS GROUPBY SALES ANALYSIS SYSTEM")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        dataset = load_dataset(file_path)
        print("\nDataset Preview:")
        print(dataset.head())
        sales_summary = analyze_sales_by_region(dataset)
        display_results(sales_summary)
    except FileNotFoundError:
        print("CSV file not found. Please check the file path.")
    except Exception as e:
        print(f"Error occurred: {e}")
if __name__ == "__main__":
    main()