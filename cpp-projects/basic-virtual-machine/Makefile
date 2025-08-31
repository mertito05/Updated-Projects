# Makefile for Basic Virtual Machine

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = vm.exe
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
