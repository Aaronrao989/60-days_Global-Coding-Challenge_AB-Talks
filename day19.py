import numpy as np
def normalize_vector(arr):
    """Convert values into probability distribution"""
    return arr / arr.sum()
def probability_examples():
    print("\n" + "=" * 70)
    print("PROBABILITY ANALYSIS USING NUMPY (NORMALIZED VECTORS)")
    print("=" * 70)
    print("\n Coin Toss (Head / Tail)")
    coin = np.array([1, 1])  # Equal chances
    coin_prob = normalize_vector(coin)
    print("Probability Distribution:", coin_prob)
    print("\n Dice Roll (1–6)")
    dice = np.array([1, 1, 1, 1, 1, 1])
    dice_prob = normalize_vector(dice)
    print("Probability Distribution:", dice_prob)
    print("\n Student Result (Pass / Fail)")
    students = np.array([70, 30])  # 70 pass, 30 fail
    student_prob = normalize_vector(students)
    print("Probability Distribution:", student_prob)
    print("\n Weather Prediction (Rain / No Rain)")
    weather = np.array([12, 18])  
    weather_prob = normalize_vector(weather)
    print("Probability Distribution:", weather_prob)
    print("\n Manufacturing Quality")
    products = np.array([5, 195]) 
    product_prob = normalize_vector(products)
    print("Probability Distribution:", product_prob)
    print("\n" + "-" * 70)
    print("Probability Analysis Completed Successfully.")
if __name__ == "__main__":
    probability_examples()