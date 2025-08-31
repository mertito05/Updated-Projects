#!/bin/bash

echo "Testing all Rust network protocol projects..."

# Test HTTPS Server
echo "Testing HTTPS Server..."
cd https-server
if cargo build; then
    echo "✓ HTTPS Server compiles successfully"
else
    echo "✗ HTTPS Server compilation failed"
fi
cd ..

# Test FTP Server
echo "Testing FTP Server..."
cd ftp-server
if cargo build; then
    echo "✓ FTP Server compiles successfully"
else
    echo "✗ FTP Server compilation failed"
fi
cd ..

# Test SSH Server
echo "Testing SSH Server..."
cd ssh-server
if cargo build; then
    echo "✓ SSH Server compiles successfully"
else
    echo "✗ SSH Server compilation failed"
fi
cd ..

# Test SMTP Server
echo "Testing SMTP Server..."
cd smtp-server
if cargo build; then
    echo "✓ SMTP Server compiles successfully"
else
    echo "✗ SMTP Server compilation failed"
fi
cd ..

# Test DNS Server
echo "Testing DNS Server..."
cd dns-server
if cargo build; then
    echo "✓ DNS Server compiles successfully"
else
    echo "✗ DNS Server compilation failed"
fi
cd ..

# Test Raw Sockets
echo "Testing Raw Sockets..."
cd raw-sockets
if cargo build; then
    echo "✓ Raw Sockets compiles successfully"
else
    echo "✗ Raw Sockets compilation failed"
fi
cd ..

echo "All projects tested!"
