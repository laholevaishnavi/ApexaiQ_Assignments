# Step 1: Create a file in root folder
with open("my_file.txt", "w", encoding="utf-8") as f:
    f.write("Hello, ApexA IQ Internship!\n")
    f.write("This is my first file handling example.\n")
print("✅ File created and data written in root folder.")

# Step 2: Read the file
with open("my_file.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("\n📖 Reading File Content:")
print(content)

# Step 3: Append data to the file
with open("my_file.txt", "a", encoding="utf-8") as f:
    f.write("Now I am appending more text to the file.\n")
print("✅ Data appended successfully.")

# Step 4: Read again to see changes
with open("my_file.txt", "r", encoding="utf-8") as f:
    print("\n📖 Updated File Content:")
    print(f.read())

# Step 5: Modify the file completely (overwrite)
with open("my_file.txt", "w", encoding="utf-8") as f:
    f.write("This is NEW content. Old content is gone.\n")
print("✅ File overwritten with new content.")


# Step 6: Reading a file OUTSIDE root directory
# Change the path below to a file on YOUR computer
external_file_path = r"C:/Users/Gaurav's Device/Desktop/ToDo.txt"

import os
if os.path.exists(external_file_path):
    with open(external_file_path, "r", encoding="utf-8") as f:
        print("\n📂 External File Content:")
        print(f.read())
else:
    print("\n⚠ The external file path is wrong or file does not exist.")
