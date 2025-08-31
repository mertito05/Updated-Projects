# Makefile for Voice Recognition Application

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = voice_recognition.exe
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

clean:
	del $(TARGET)

.PHONY: clean
