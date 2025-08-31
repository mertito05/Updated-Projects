# Makefile for Basic Operating System Simulation

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = os_simulation
SRC = main.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)

.PHONY: clean
