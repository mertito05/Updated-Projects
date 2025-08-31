# Makefile for Simple Calendar Application

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = calendar
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
