# Lab 3: Data Structures and Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Task 1: Explore set methods
print("Set methods:")
s = {1, 2, 3}
print("Original set:", s)
s.add(4)
print("After add(4):", s)
s.remove(2)
print("After remove(2):", s)
print("Union:", s.union({5, 6}))
print("Intersection:", s.intersection({3, 4, 5}))

# Task 2: Explore dict methods
print("\nDict methods:")
d = {'a': 1, 'b': 2}
print("Original dict:", d)
d['c'] = 3
print("After adding 'c':", d)
print("Keys:", list(d.keys()))
print("Values:", list(d.values()))
print("Items:", list(d.items()))

# Task 3: Convert between types
print("\nType conversions:")
lst = [1, 2, 3]
print("List to tuple:", tuple(lst))
print("List to set:", set(lst))
tup = (4, 5, 6)
print("Tuple to list:", list(tup))
print("Tuple to set:", set(tup))

# Task 4: Default arguments
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print("\nDefault arguments:")
print(greet("Alice"))
print(greet("Bob", "Hi"))

# Task 5: File operations
print("\nFile operations:")
# Write to file
with open('sample.txt', 'w') as f:
    f.write("Hello, World!\n")
    f.write("This is a test file.")

# Read from file
with open('sample.txt', 'r') as f:
    content = f.read()
    print("File content:", content)

# Task 6: Matplotlib plot
print("\nMatplotlib plot:")
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.show()

# Task 7: Pandas data
print("\nPandas DataFrame:")
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35], 'City': ['NY', 'LA', 'Chicago']}
df = pd.DataFrame(data)
print(df)
print("Mean age:", df['Age'].mean())
print("Names:", df['Name'].tolist())
