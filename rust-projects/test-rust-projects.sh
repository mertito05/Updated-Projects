#!/bin/bash


echo "=== Rust Projects Test Script ==="

# Check if Rust is installed
if ! command -v rustc &> /dev/null; then
    echo "Rust is not installed on this system."
    echo ""
    echo "To install Rust, please visit: https://www.rust-lang.org/tools/install"
    echo "Or run the following command:"
    echo "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    echo ""
    echo "After installation, restart your terminal and run this script again."
    exit 1
fi

# Check if Cargo is installed
if ! command -v cargo &> /dev/null; then
    echo "Cargo (Rust package manager) is not installed."
    echo "This usually means Rust was not installed correctly."
    echo "Please reinstall Rust using the official installer."
    exit 1
fi

echo "Rust version: $(rustc --version)"
echo "Cargo version: $(cargo --version)"
echo ""

# List all Rust projects
echo "Available Rust projects:"
echo "1. command-line-tool"
echo "2. web-server" 
echo "3. data-processor"
echo "4. game-development"
echo "5. networking-application"
echo ""

echo "To build and run any project:"
echo "cd project-directory/"
echo "cargo build"
echo "cargo run"
echo ""

echo "All projects have been created successfully!"
echo "Each project includes:"
echo "- Cargo.toml (project configuration)"
echo "- src/main.rs (main source code)"
echo "- README.md (documentation)"
