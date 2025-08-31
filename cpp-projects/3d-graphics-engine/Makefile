# Makefile for 3D Graphics Engine

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = engine.exe
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
