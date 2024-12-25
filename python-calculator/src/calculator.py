from operations.basic import add, subtract, multiply, divide
from operations.advanced import power, square_root, logarithm

def main():
    print("Welcome to the Advanced Calculator!")
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Logarithm")

    while True:
        choice = input("Enter choice (1-7): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"{num1} / {num2} = {divide(num1, num2)}")

        elif choice in ['5', '6', '7']:
            num = float(input("Enter number: "))

            if choice == '5':
                exponent = float(input("Enter exponent: "))
                print(f"{num} ^ {exponent} = {power(num, exponent)}")
            elif choice == '6':
                print(f"Square root of {num} = {square_root(num)}")
            elif choice == '7':
                base = float(input("Enter base: "))
                print(f"Logarithm of {num} with base {base} = {logarithm(num, base)}")

        else:
            print("Invalid input")

        next_calculation = input("Do you want to perform another calculation? (yes/no): ")
        if next_calculation.lower() != 'yes':
            break

if __name__ == "__main__":
    main()