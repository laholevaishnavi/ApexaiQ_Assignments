# using pathlib
from pathlib import Path

# Step 1: Create a file in root folder
root_file = Path("my_file.txt")

# 'w' mode will create the file if it doesn't exist
with root_file.open("w", encoding="utf-8") as f:
    f.write("Hello, ApexA IQ Internship!\n")
    f.write("This is my first file handling example.\n")
print("✅ File created and data written in root folder.")

# Step 2: Read the file
with root_file.open("r", encoding="utf-8") as f:
    content = f.read()
print("\n📖 Reading File Content:")
print(content)

# Step 3: Append data to the file
with root_file.open("a", encoding="utf-8") as f:
    f.write("Now I am appending more text to the file.\n")
print("✅ Data appended successfully.")

# Step 4: Read again to see changes
with root_file.open("r", encoding="utf-8") as f:
    print("\n📖 Updated File Content:")
    print(f.read())

# Step 5: Modify the file completely (overwrite)
with root_file.open("w", encoding="utf-8") as f:
    f.write("This is NEW content. Old content is gone.\n")
print("✅ File overwritten with new content.")

# Step 6: Reading a file OUTSIDE root directory
# Change the path below to a file on YOUR computer
external_file = Path(r"C:/Users/Gaurav's Device/Desktop/ToDo.txt")

if external_file.exists():
    with external_file.open("r", encoding="utf-8") as f:
        print("\n📂 External File Content:")
        print(f.read())
else:
    print("\n⚠ The external file path is wrong or file does not exist.")
