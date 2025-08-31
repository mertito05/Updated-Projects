# Makefile for Simple Music Player

CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = music_player
SRC = main.c

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
