# Makefile for Machine Learning Model

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = ml_model.exe
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
