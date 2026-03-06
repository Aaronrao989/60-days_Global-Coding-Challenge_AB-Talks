def calculate_sales(sales_data):
    total_sales = 0

    for sale in sales_data:
        total_sales += sale

    average_sales = total_sales / len(sales_data)

    return total_sales, average_sales


def main():
    print("\n" + "=" * 70)
    print("WEEKLY SALES ANALYSIS SYSTEM")
    print("=" * 70)

    sales_data = []
    
    for day in range(1, 8):
        sale = float(input(f"Enter sales for Day {day} (₹): "))
        sales_data.append(sale)

    total_sales, average_sales = calculate_sales(sales_data)

    print("\n" + "-" * 70)
    print("WEEKLY SALES SUMMARY")
    print("-" * 70)

    for i, sale in enumerate(sales_data, start=1):
        print(f"Day {i} Sales{'':<14}: ₹{sale:,.2f}")

    print("-" * 70)
    print(f"{'Total Weekly Sales':<25}: ₹{total_sales:,.2f}")
    print(f"{'Average Daily Sales':<25}: ₹{average_sales:,.2f}")
    print("-" * 70)
    print("Sales Analysis Completed Successfully.")


if __name__ == "__main__":
    main()