# Makefile for Personal Finance Tracker

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = finance_tracker
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
