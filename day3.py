def classify_result(marks):
    if marks >= 40:
        return "PASS"
    else:
        return "FAIL"
def main():
    print("\n" + "=" * 70)
    print("STUDENT RESULT CLASSIFICATION SYSTEM")
    print("=" * 70)
    student_name = input("\nEnter Student Name: ")
    student_id = input("Enter Student ID: ")
    marks = float(input("Enter Student Marks: "))
    result = classify_result(marks)
    print("\n" + "-" * 70)
    print("RESULT SUMMARY")
    print("-" * 70)
    print(f"{'Student Name':<25}: {student_name}")
    print(f"{'Student ID':<25}: {student_id}")
    print(f"{'Marks Obtained':<25}: {marks}")
    print(f"{'Result':<25}: {result}")
    print("-" * 70)
    print("Result Generated Successfully.")
main()