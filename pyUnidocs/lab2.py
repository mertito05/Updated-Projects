# Lab 2: Introduction to Python - Strings, NumPy, NLTK

import numpy as np
import nltk
from nltk.book import *

# Task 1: Count words longer than 10 in text1
long_words = [w for w in text1 if len(w) > 10]
print("Number of words longer than 10 in text1:", len(long_words))

# Task 2: Frequency of words in 'news' genre of brown corpus
from nltk.corpus import brown
news_words = brown.words(categories='news')
fd = nltk.FreqDist(news_words)
print("Top 10 words in news category:")
for word, freq in fd.most_common(10):
    print(f"{word}: {freq}")

# Task 3: Function to check palindrome
def is_palindrome(word):
    return word == word[::-1]

print("Is 'aba' a palindrome?", is_palindrome("aba"))
print("Is 'hello' a palindrome?", is_palindrome("hello"))

# Task 4: GCD function
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print("GCD of 48 and 18:", gcd(48, 18))
print("GCD of 100 and 75:", gcd(100, 75))
