def calculate_mean(numbers):
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    if n % 2 == 0:
        mid1 = sorted_numbers[n // 2 - 1]
        mid2 = sorted_numbers[n // 2]
        return (mid1 + mid2) / 2
    else:
        return sorted_numbers[n // 2]


def calculate_mode(numbers):
    frequency = {}
    
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    max_count = max(frequency.values())
    modes = [num for num, count in frequency.items() if count == max_count]

    return modes


def main():
    print("\n" + "=" * 70)
    print("STATISTICAL ANALYSIS SYSTEM")
    print("=" * 70)

    numbers = list(map(float, input("\nEnter numbers separated by space: ").split()))

    mean_value = calculate_mean(numbers)
    median_value = calculate_median(numbers)
    mode_value = calculate_mode(numbers)

    print("\n" + "-" * 70)
    print("STATISTICAL SUMMARY")
    print("-" * 70)

    print(f"{'Dataset':<20}: {numbers}")
    print(f"{'Mean':<20}: {mean_value:.2f}")
    print(f"{'Median':<20}: {median_value:.2f}")
    print(f"{'Mode':<20}: {mode_value}")

    print("-" * 70)
    print("Statistical Analysis Completed Successfully.")


if __name__ == "__main__":
    main()