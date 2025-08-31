# Lab 1: Introduction to Python
# Basic Python concepts: variables, data types, operators, control structures

# Variables and data types
print("Hello, World!")

x = 5
y = "Python"
z = 3.14
is_active = True

print("Integer:", x)
print("String:", y)
print("Float:", z)
print("Boolean:", is_active)

# Basic operators
print("Addition:", x + 5)
print("String concatenation:", y + " programming")
print("Float multiplication:", z * 2)

# Lists
fruits = ["apple", "banana", "cherry"]
print("List:", fruits)
print("First fruit:", fruits[0])

# Dictionaries
person = {"name": "John", "age": 30, "city": "New York"}
print("Dictionary:", person)
print("Name:", person["name"])

# Control structures
if x > 3:
    print("x is greater than 3")
else:
    print("x is not greater than 3")

for fruit in fruits:
    print("Fruit:", fruit)

# Functions
def greet(name):
    return "Hello, " + name

print(greet("Alice"))
