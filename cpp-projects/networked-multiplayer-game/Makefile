# Makefile for Networked Multiplayer Game

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET_SERVER = server.exe
TARGET_CLIENT = client.exe
SRC_SERVER = server.cpp
SRC_CLIENT = client.cpp

all: $(TARGET_SERVER) $(TARGET_CLIENT)

$(TARGET_SERVER): $(SRC_SERVER)
	$(CXX) $(CXXFLAGS) -o $(TARGET_SERVER) $(SRC_SERVER)

$(TARGET_CLIENT): $(SRC_CLIENT)
	$(CXX) $(CXXFLAGS) -o $(TARGET_CLIENT) $(SRC_CLIENT)

clean:
	del $(TARGET_SERVER) $(TARGET_CLIENT)

.PHONY: clean
