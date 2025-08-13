#Error Handling Basics

# ----------------
# Example1
# ----------------

try:
    # Code that may cause error
    num = int(input("Enter a number: "))
    print("You entered:", num)
except:
    # Code to run if error occurs
    print("Oops! That was not a valid number.")


# ----------------
# Example2
# ----------------

try:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))
    result = num1 / num2
    print("Result:", result)
except ValueError:
    print("Please enter numbers only!")
except ZeroDivisionError:
    print("You cannot divide by zero.")


# ----------------
# ERROR HANDLING in File Handling
# ----------------
try:
    # Attempt to open file in read mode
    file = open("sample.txt", "r")
    
    # If no error, read the file
    content = file.read()
    print("✅ File content:")
    print(content)

except FileNotFoundError:
    # Specific error handling for missing file
    print("Error: The file 'sample.txt' was not found.")

except PermissionError:
    # If you don't have permission to open file
    print("Error: You don't have permission to open this file.")

except Exception as e:
    # Catch any other type of error
    print(f"An unexpected error occurred: {e}")

else:
    # Runs only if try block has NO error
    print("✅ File read successfully!")

finally:
    # This will run no matter what
    try:
        file.close()
        print("🔒 File closed.")
    except NameError:
        # If file variable was never created
        print("ℹ No file to close.")



# ----------------
# Example-4
# ----------------

try:
    num = int(input("Enter a positive number: "))
    if num < 0:
        raise ValueError("Negative number not allowed!")  # Custom error
except ValueError as e:
    print("Error:", e)
else:
    print("Great! No errors found.")
finally:
    print("This will always run, even if error occurs.")
