import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

def main():
    print("\n" + "=" * 70)
    print("ADVANCED TIME SERIES ANALYSIS (DECOMPOSITION + ARIMA)")
    print("=" * 70)
    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day38/sales_data.csv")

    print("\nDataset Preview:")
    print(df.head())
    df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
    df.set_index("Sale_Date", inplace=True)
    monthly_sales = df["Sales_Amount"].resample("ME").sum()

    print("\nMonthly Sales Preview:")
    print(monthly_sales.head())
    print("\nPerforming decomposition...")
    period = min(6, len(monthly_sales)//2)

    print(f"Using period: {period}")

    decomposition = seasonal_decompose(
        monthly_sales,
        model='additive',
        period=period
    )

    decomposition.plot()
    plt.suptitle("Trend, Seasonality, Residuals")
    plt.tight_layout()
    plt.show()

    print("\nTraining ARIMA model...")

    model = ARIMA(monthly_sales, order=(1, 1, 1))
    model_fit = model.fit()

    print("\nModel Summary:")
    print(model_fit.summary())
    forecast_steps = 6
    forecast = model_fit.forecast(steps=forecast_steps)

    print("\nForecasted Values:")
    print(forecast)

    plt.figure()

    plt.plot(monthly_sales, label="Actual")
    plt.plot(forecast, label="Forecast", linestyle='--')

    plt.title("ARIMA Forecast (Next 6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\nTime Series Analysis Completed Successfully 🚀")

if __name__ == "__main__":
    main()