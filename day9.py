import numpy as np
def matrix_operations(matrix_a, matrix_b):
    addition = matrix_a + matrix_b
    multiplication = np.matmul(matrix_a, matrix_b)
    return addition, multiplication
def get_matrix(rows, cols, name):
    matrix = []
    print(f"\nEnter values for {name}:")
    for i in range(rows):
        while True:
            row = list(map(float, input(f"Row {i+1} (enter {cols} values): ").split()))
            if len(row) != cols:
                print(f"⚠ Please enter exactly {cols} values separated by spaces.")
            else:
                matrix.append(row)
                break
    return np.array(matrix)

def display_results(matrix_a, matrix_b, addition, multiplication):
    print("\n" + "-" * 70)
    print("MATRIX OPERATION RESULTS")
    print("-" * 70)
    print("\nMatrix A:")
    print(matrix_a)
    print("\nMatrix B:")
    print(matrix_b)
    print("\nMatrix Addition (A + B):")
    print(addition)
    print("\nMatrix Multiplication (A × B):")
    print(multiplication)
    print("\n" + "-" * 70)
    print("Matrix Operations Completed Successfully.")

def main():
    print("\n" + "=" * 70)
    print("NUMPY MATRIX OPERATIONS SYSTEM")
    print("=" * 70)
    rows = int(input("\nEnter number of rows for matrices: "))
    cols = int(input("Enter number of columns for matrices: "))
    matrix_a = get_matrix(rows, cols, "Matrix A")
    matrix_b = get_matrix(rows, cols, "Matrix B")
    addition, multiplication = matrix_operations(matrix_a, matrix_b)
    display_results(matrix_a, matrix_b, addition, multiplication)

if __name__ == "__main__":
    main()