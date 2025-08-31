import socket
import threading
import sys

def receive_messages(client_socket):
    """Receive messages from the server"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n{message}")
            print("You: ", end="", flush=True)
        except:
            print("Disconnected from server")
            break

def start_client():
    """Start the chat client"""
    host = input("Enter server IP (default: localhost): ") or 'localhost'
    port = 12345
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        # Get username
        username = input("Enter your username: ")
        client_socket.send(username.encode('utf-8'))
        
        print(f"Connected to {host}:{port}")
        print("Type your messages. Type '/quit' to exit.")
        print("-" * 50)
        
        # Start receiving messages in a separate thread
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        # Send messages
        while True:
            message = input("You: ")
            if message.lower() == '/quit':
                break
            client_socket.send(message.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    """Start the chat server"""
    host = '0.0.0.0'
    port = 12345
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Server started on {host}:{port}")
    print("Waiting for connections...")
    
    clients = []
    usernames = []
    
    def broadcast(message, sender_socket=None):
        """Send message to all clients except sender"""
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    clients.remove(client)
    
    def handle_client(client_socket):
        """Handle client connection"""
        try:
            # Get username
            username = client_socket.recv(1024).decode('utf-8')
            usernames.append(username)
            clients.append(client_socket)
            
            print(f"{username} joined the chat")
            broadcast(f"{username} joined the chat", client_socket)
            
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                if message.lower() == '/quit':
                    break
                
                full_message = f"{username}: {message}"
                print(full_message)
                broadcast(full_message, client_socket)
                
        except:
            pass
        finally:
            if client_socket in clients:
                clients.remove(client_socket)
                if username in usernames:
                    usernames.remove(username)
                print(f"{username} left the chat")
                broadcast(f"{username} left the chat")
                client_socket.close()
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

def main():
    """Main function"""
    print("=== Chat Application ===")
    print("1. Start Server")
    print("2. Start Client")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        start_server()
    elif choice == "2":
        start_client()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
