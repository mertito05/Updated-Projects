#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <string>
#include <thread>
#include <vector>

#pragma comment(lib, "ws2_32.lib")

class GameServer {
private:
    SOCKET serverSocket;
    std::vector<SOCKET> clients;
    
public:
    GameServer() : serverSocket(INVALID_SOCKET) {}
    
    bool initialize() {
        WSADATA wsaData;
        int result = WSAStartup(MAKEWORD(2, 2), &wsaData);
        if (result != 0) {
            std::cerr << "WSAStartup failed: " << result << std::endl;
            return false;
        }
        
        serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (serverSocket == INVALID_SOCKET) {
            std::cerr << "Socket creation failed: " << WSAGetLastError() << std::endl;
            WSACleanup();
            return false;
        }
        
        sockaddr_in serverAddr;
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_addr.s_addr = INADDR_ANY;
        serverAddr.sin_port = htons(12345);
        
        if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
            std::cerr << "Bind failed: " << WSAGetLastError() << std::endl;
            closesocket(serverSocket);
            WSACleanup();
            return false;
        }
        
        if (listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) {
            std::cerr << "Listen failed: " << WSAGetLastError() << std::endl;
            closesocket(serverSocket);
            WSACleanup();
            return false;
        }
        
        return true;
    }
    
    void run() {
        std::cout << "Server started on port 12345" << std::endl;
        
        while (true) {
            sockaddr_in clientAddr;
            int clientAddrSize = sizeof(clientAddr);
            
            SOCKET clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientAddrSize);
            if (clientSocket == INVALID_SOCKET) {
                std::cerr << "Accept failed: " << WSAGetLastError() << std::endl;
                continue;
            }
            
            clients.push_back(clientSocket);
            std::cout << "Client connected. Total clients: " << clients.size() << std::endl;
            
            // Handle client in a separate thread
            std::thread([this, clientSocket]() {
                handleClient(clientSocket);
            }).detach();
        }
    }
    
    void handleClient(SOCKET clientSocket) {
        char buffer[1024];
        int bytesReceived;
        
        while (true) {
            bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
            if (bytesReceived <= 0) {
                break;
            }
            
            buffer[bytesReceived] = '\0';
            std::cout << "Received: " << buffer << std::endl;
            
            // Echo back to client
            send(clientSocket, buffer, bytesReceived, 0);
        }
        
        // Remove client from list
        auto it = std::find(clients.begin(), clients.end(), clientSocket);
        if (it != clients.end()) {
            clients.erase(it);
        }
        
        closesocket(clientSocket);
        std::cout << "Client disconnected. Total clients: " << clients.size() << std::endl;
    }
    
    ~GameServer() {
        for (SOCKET client : clients) {
            closesocket(client);
        }
        closesocket(serverSocket);
        WSACleanup();
    }
};

int main() {
    GameServer server;
    
    if (!server.initialize()) {
        return 1;
    }
    
    server.run();
    return 0;
}
