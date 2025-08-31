#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <thread>

#pragma comment(lib, "ws2_32.lib")

class GameClient {
private:
    SOCKET clientSocket;
    
public:
    GameClient() : clientSocket(INVALID_SOCKET) {}
    
    bool connectToServer(const std::string& serverIP, int port) {
        WSADATA wsaData;
        int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
        if (result != 0) {
            std::cerr << "WSAStartup failed: " << result << std::endl;
            return false;
        }
        
        clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (clientSocket == INVALID_SOCKET) {
            std::cerr << "Socket creation failed: " << WSAGetLastError() << std::endl;
            WSACleanup();
            return false;
        }
        
        sockaddr_in serverAddr;
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(port);
        inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr);
        
        if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
            std::cerr << "Connect failed: " << WSAGetLastError() << std::endl;
            closesocket(clientSocket);
            WSACleanup();
            return false;
        }
        
        std::cout << "Connected to server " << serverIP << ":" << port << std::endl;
        return true;
    }
    
    void start() {
        // Thread for receiving messages
        std::thread receiveThread([this]() {
            receiveMessages();
        });
        
        // Main thread for sending messages
        sendMessages();
        
        receiveThread.join();
    }
    
    void sendMessages() {
        std::string message;
        while (true) {
            std::cout << "Enter message (or 'quit' to exit): ";
            std::getline(std::cin, message);
            
            if (message == "quit") {
                break;
            }
            
            if (send(clientSocket, message.c_str(), message.length(), 0) == SOCKET_ERROR) {
                std::cerr << "Send failed: " << WSAGetLastError() << std::endl;
                break;
            }
        }
        
        closesocket(clientSocket);
        WSACleanup();
    }
    
    void receiveMessages() {
        char buffer[1024];
        int bytesReceived;
        
        while (true) {
            bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
            if (bytesReceived <= 0) {
                std::cout << "Disconnected from server" << std::endl;
                break;
            }
            
            buffer[bytesReceived] = '\0';
            std::cout << "Server: " << buffer << std::endl;
        }
    }
    
    ~GameClient() {
        if (clientSocket != INVALID_SOCKET) {
            closesocket(clientSocket);
        }
        WSACleanup();
    }
};

int main() {
    GameClient client;
    
    if (!client.connectToServer("127.0.0.1", 12345)) {
        return 1;
    }
    
    client.start();
    return 0;
}
