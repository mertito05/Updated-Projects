# Makefile for 2D Game Development

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11 `sdl2-config --cflags`
LDFLAGS = `sdl2-config --libs`
TARGET = game
SRC = main.cpp

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: clean
