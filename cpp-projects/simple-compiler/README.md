# Simple Compiler for a Custom Language

A basic compiler implementation in C++ that translates a simple custom language into executable code or intermediate representation.

## Features

- Lexical analysis (tokenization)
- Syntax analysis (parsing)
- Simple semantic analysis
- Code generation

## Language Syntax

The custom language supports:
- Variable declarations
- Arithmetic operations
- Conditional statements
- Basic I/O operations

## Usage

1. Compile the compiler:
   ```bash
   g++ main.cpp -o compiler
   ```

2. Run the compiler:
   ```bash
   ./compiler
   ```

## Example Input

```
x = 5
y = 10
z = x + y
print z
```

## Future Enhancements

- Support for functions
- More data types
- Error reporting
- Optimization passes
- Target different output formats
