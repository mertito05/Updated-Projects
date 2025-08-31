# Rust Calculator

A comprehensive command-line calculator written in Rust with multiple calculation modes.

## Features

- **Basic Arithmetic**: Addition, subtraction, multiplication, division, and modulo
- **Scientific Functions**: Square root, power, trigonometric functions, logarithms
- **Unit Conversion**: Temperature, length, and weight conversions
- **Error Handling**: Proper error handling for invalid inputs and operations

## Usage

1. Compile the project:
   ```bash
   cargo build
   ```

2. Run the executable:
   ```bash
   cargo run
   ```

3. Follow the interactive menu:
   - Choose option 1 for Basic Arithmetic
   - Choose option 2 for Scientific Functions
   - Choose option 3 for Unit Conversion
   - Choose option 4 to Exit

## Examples

### Basic Arithmetic
```bash
Enter first number: 10
Enter operator (+, -, *, /, %): *
Enter second number: 5
Result: 10 * 5 = 50
```

### Scientific Functions
```bash
Choose a function: 1  (Square root)
Enter number: 16
sqrt(16) = 4
```

### Unit Conversion
```bash
Choose conversion: 1  (Celsius to Fahrenheit)
Enter value: 25
25 °C = 77.00 °F
```

## Available Functions

### Basic Arithmetic
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)
- Modulo (%)

### Scientific Functions
- Square root (sqrt)
- Power (pow)
- Sine (sin)
- Cosine (cos)
- Tangent (tan)
- Base-10 logarithm (log10)
- Natural logarithm (ln)

### Unit Conversions
- Celsius to Fahrenheit
- Fahrenheit to Celsius
- Meters to Feet
- Feet to Meters
- Kilograms to Pounds
- Pounds to Kilograms

## Error Handling

The calculator includes comprehensive error handling:
- Division by zero protection
- Negative number validation for square roots and logarithms
- Invalid operator detection
- Input parsing errors

## Additional Utilities

The calculator also includes utility functions:
- `factorial(n)` - Calculates factorial of a number
- `calculate_bmi(weight_kg, height_m)` - Calculates Body Mass Index

## Dependencies

- Standard Rust library only (no external dependencies)
- Uses Rust's built-in mathematical functions

## Building

```bash
cargo build --release
```

The executable will be available in `target/release/calculator`

## Features

- **Interactive Menu**: Easy-to-use text-based interface
- **Precision**: Uses f64 floating-point numbers for accurate calculations
- **Safety**: Rust's type system ensures memory safety
- **Portable**: No external dependencies, runs anywhere Rust is supported

## Limitations

- Basic command-line interface
- No graphical user interface
- No calculation history
- No complex expression parsing (single operations only)

## Extending

The calculator can be easily extended by:
- Adding more mathematical functions
- Implementing expression parsing
- Adding more unit conversions
- Creating a graphical interface
