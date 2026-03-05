def calculate_tax(annual_salary):
    if annual_salary <= 250000:
        return 0
    elif annual_salary <= 500000:
        return (annual_salary - 250000) * 0.05
    elif annual_salary <= 1000000:
        return (250000 * 0.05) + (annual_salary - 500000) * 0.20
    else:
        return (250000 * 0.05) + (500000 * 0.20) + (annual_salary - 1000000) * 0.30


def main():
    print("\n" + "=" * 70)
    print("EMPLOYEE SALARY REPORT SYSTEM")
    print("=" * 70)

    employee_name = input("\nEnter Employee Name: ")
    employee_id = input("Enter Employee ID: ")
    monthly_salary = float(input("Enter Monthly Salary (₹): "))

    annual_salary = monthly_salary * 12
    tax_amount = calculate_tax(annual_salary)
    net_annual_salary = annual_salary - tax_amount

    print("\n" + "-" * 70)
    print("SALARY SUMMARY")
    print("-" * 70)

    print(f"{'Employee Name':<25}: {employee_name}")
    print(f"{'Employee ID':<25}: {employee_id}")
    print(f"{'Monthly Salary':<25}: ₹{monthly_salary:,.2f}")
    print(f"{'Annual Salary':<25}: ₹{annual_salary:,.2f}")
    print(f"{'Tax Deducted':<25}: ₹{tax_amount:,.2f}")
    print(f"{'Net Annual Salary':<25}: ₹{net_annual_salary:,.2f}")

    print("-" * 70)
    print("Report Generated Successfully.")


main()