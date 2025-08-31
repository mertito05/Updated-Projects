# Makefile for Web Scraper

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = webscraper.exe
SRC = main.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
