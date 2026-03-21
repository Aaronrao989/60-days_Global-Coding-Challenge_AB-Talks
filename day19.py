def probability_examples():
    print("\n" + "=" * 70)
    print("PROBABILITY ANALYSIS - REAL LIFE EXAMPLES")
    print("=" * 70)
    print("\n 1️⃣ Coin Toss Probability")
    total_outcomes = 2  
    favorable = 1       
    prob = favorable / total_outcomes
    print(f"Probability of getting Head: {prob:.2f}")
    print("\n 2️⃣ Dice Roll Probability")
    total_outcomes = 6
    favorable = 2 
    prob = favorable / total_outcomes
    print(f"Probability of getting an even number (2 or 4): {prob:.2f}")
    print("\n 3️⃣ Student Passing Probability")
    total_students = 100
    passed_students = 70
    prob = passed_students / total_students
    print(f"Probability of a student passing: {prob:.2f}")
    print("\n 4️⃣ Weather Prediction")
    rainy_days = 12
    total_days = 30
    prob = rainy_days / total_days
    print(f"Probability of rain on a given day: {prob:.2f}")
    print("\n 5️⃣ Quality Control in Manufacturing")
    defective = 5
    total_products = 200
    prob = defective / total_products
    print(f"Probability of a product being defective: {prob:.3f}")
    print("\n" + "-" * 70)
    print("Probability Analysis Completed Successfully.")
if __name__ == "__main__":
    probability_examples()