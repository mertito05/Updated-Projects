#!/bin/bash

# Test script for Inventory Management System
echo "=== Testing Inventory Management System ==="

# Compile the program
echo "Compiling..."
gcc -Wall -Wextra -std=c99 -o inventory main.c
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi
echo "Compilation successful!"

# Test 1: Display empty inventory
echo -e "\nTest 1: Display empty inventory"
echo "2" | ./inventory

# Test 2: Add items
echo -e "\nTest 2: Adding items"
echo -e "1\nLaptop\n5\n999.99\n2\n1\nMouse\n10\n25.50\n2\n1\nKeyboard\n8\n45.75\n2" | ./inventory

# Test 3: Search for existing item
echo -e "\nTest 3: Search for existing item"
echo -e "3\nLaptop\n5" | ./inventory

# Test 4: Search for non-existing item
echo -e "\nTest 4: Search for non-existing item"
echo -e "3\nMonitor\n5" | ./inventory

# Test 5: Update item
echo -e "\nTest 5: Update item"
echo -e "4\n1\n15\n899.99\n2\n5" | ./inventory

# Test 6: Invalid menu choice
echo -e "\nTest 6: Invalid menu choice"
echo -e "9\n5" | ./inventory

# Test 7: Exit program
echo -e "\nTest 7: Exit program"
echo -e "5" | ./inventory

echo -e "\n=== All tests completed ==="
