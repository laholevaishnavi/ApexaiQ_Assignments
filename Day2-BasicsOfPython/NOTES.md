# ApexaiQ Internship - Python Learning Tasks

This repository contains Python programs and research notes for my daily internship tasks at **ApexA IQ**.

## [13-08-2025] Topics covered

1. **List Comprehension**
2. **Dict Comprehension**
3. **File Handling**
4. **Error Handling**

---

## 📚 Research Notes

There are four collection data types in the Python programming language:

List is a collection which is ordered and changeable. Allows duplicate members.

Tuple is a collection which is ordered and unchangeable. Allows duplicate members.

Set is a collection which is unordered, unchangeable\*, and unindexed. No duplicate members.

Dictionary is a collection which is ordered\*\* and changeable. No duplicate membe

### 1. List Comprehension

A concise way to create lists using a single line.

Syntax: [expression for item in iterable if condition]

```python
[x**2 for x in range(10) if x % 2 == 0]

```

### 2. Dictionary Comprehension

A compact way to create dictionaries.

Syntax: {key_expression: value_expression for item in iterable if condition}

```python
squares = {x: x**2 for x in range(5)}
```

### 3. File Handling

## File Handling in Python

File handling allows reading, writing, and managing files from Python code.

## File handling operations

```python
f = open("file.txt", "r")   # r = read, w = write, a = append, b = binary
data = f.read()     # Reads entire file
line = f.readline() # Reads one line
lines = f.readlines() # Reads all lines into a list
f = open("file.txt", "w")
f.write("Hello World")
f.close()

```

## Using with (Auto Close)

```python
with open("file.txt", "r") as f:
    data = f.read()

```

## Path Handling

Use pathlib for OS-independent paths:

```python
from pathlib import Path
file_path = Path("folder") / "file.txt"
```

### 3. Error Handling

Error handling is the process of managing unexpected situations (errors or exceptions) in a program without crashing it. In Python, we handle errors using the try-except block.

```python
try:
    # Code that might cause an error
except ExceptionType:
    # Code that runs if error occurs
    
```

##Common Exception Types

ZeroDivisionError → Dividing by zero.

ValueError → Wrong value type.

FileNotFoundError → Missing file.

TypeError → Wrong data type used.

##Catching all the exceptions

```python
try:
    x = 10 / 0
except Exception as e:  # e stores error message
    print("Error:", e)  # Prints system-defined error message
```

## else & finally in Error Handling
else → Runs if no error occurs.

finally → Always runs (cleanup code, closing files, etc.).