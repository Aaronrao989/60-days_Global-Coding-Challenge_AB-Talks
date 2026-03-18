import matplotlib.pyplot as plt
def plot_sales(months, sales):
    plt.figure()
    plt.plot(months, sales, marker='o')
    plt.title("Monthly Sales Trend")
    plt.xlabel("Months")
    plt.ylabel("Sales (₹)")
    plt.grid()
    plt.show()
def main():
    n = int(input("Enter number of months: "))
    months = []
    sales = []
    for i in range(n):
        month = input(f"Enter month {i+1}: ")
        value = float(input(f"Enter sales for {month}: "))
        months.append(month)
        sales.append(value)
    plot_sales(months, sales)
if __name__ == "__main__":
    main()