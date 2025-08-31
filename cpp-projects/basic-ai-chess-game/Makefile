# Makefile for Basic AI Chess Game

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = chess.exe
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
