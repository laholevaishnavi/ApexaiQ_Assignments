# Without List Comprehension
fruits = ["apple", "banana", "grapes", "mango", "kiwi", "cherry"]
new_list = []
for fruit in fruits:
  if "a" in fruit:
    new_list.append(fruit)
print(fruits)
print(new_list)

# with List Comprehension
fruit_list = [x for x in fruits if "a" in x]
print(fruit_list)