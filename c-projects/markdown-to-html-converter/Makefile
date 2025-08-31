# Makefile for Markdown to HTML Converter

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = markdown_converter
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
