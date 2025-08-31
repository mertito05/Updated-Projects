# Makefile for Simple Database Management System

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = dbms
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
