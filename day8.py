import numpy as np
def analyze_temperatures(temp_array):
    min_temp = np.min(temp_array)
    max_temp = np.max(temp_array)
    avg_temp = np.mean(temp_array)
    return min_temp, max_temp, avg_temp

def display_report(temp_array, min_temp, max_temp, avg_temp):
    print("\n" + "-" * 70)
    print("TEMPERATURE ANALYSIS SUMMARY")
    print("-" * 70)
    print(f"{'Temperature Data':<25}: {temp_array}")
    print(f"{'Minimum Temperature':<25}: {min_temp:.2f} °C")
    print(f"{'Maximum Temperature':<25}: {max_temp:.2f} °C")
    print(f"{'Average Temperature':<25}: {avg_temp:.2f} °C")
    print("-" * 70)
    print("Temperature Analysis Completed Successfully.")

def main():
    print("\n" + "=" * 70)
    print("NUMPY TEMPERATURE ANALYSIS SYSTEM")
    print("=" * 70)
    n = int(input("\nEnter number of temperature readings: "))
    temperatures = []
    for i in range(n):
        temp = float(input(f"Enter temperature {i+1} (°C): "))
        temperatures.append(temp)
    temp_array = np.array(temperatures)
    min_temp, max_temp, avg_temp = analyze_temperatures(temp_array)
    display_report(temp_array, min_temp, max_temp, avg_temp)

if __name__ == "__main__":
    main()