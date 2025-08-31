# Makefile for Inventory Management System

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = inventory
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
