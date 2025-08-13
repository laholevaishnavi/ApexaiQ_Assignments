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
Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
Dictionary is a collection which is ordered** and changeable. No duplicate membe

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
Working with files (reading/writing) in Python.
Basic Steps:

Open a file using open(filename, mode)

Perform operations (read, write, append)

Close the file using .close() or with with statement (auto-closes file).

Modes:

'r': Read

'w': Write (overwrites)

'a': Append

'rb' / 'wb': Binary modes

Example:

```python
with open("example.txt", "w") as file:
    file.write("Hello, ApexaiQ!")
```