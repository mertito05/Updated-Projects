# Makefile for HTTP Server
CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = http-server
SRC = main.c
LIBS = -lws2_32

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LIBS)

clean:
	del $(TARGET).exe

.PHONY: all clean
