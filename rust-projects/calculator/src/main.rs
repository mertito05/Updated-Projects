use std::io::{self, Write};

fn main() {
    println!("=== Rust Calculator ===");
    println!("A simple command-line calculator");

    loop {
        println!("\nOptions:");
        println!("1. Basic Arithmetic");
        println!("2. Scientific Functions");
        println!("3. Unit Conversion");
        println!("4. Exit");
        print!("Choose an option: ");
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim();

        match choice {
            "1" => basic_arithmetic(),
            "2" => scientific_functions(),
            "3" => unit_conversion(),
            "4" => {
                println!("Goodbye!");
                break;
            }
            _ => println!("Invalid option. Please try again."),
        }
    }
}

fn basic_arithmetic() {
    println!("\n--- Basic Arithmetic ---");
    
    print!("Enter first number: ");
    io::stdout().flush().unwrap();
    let mut num1_str = String::new();
    io::stdin().read_line(&mut num1_str).unwrap();
    let num1: f64 = num1_str.trim().parse().unwrap_or(0.0);

    print!("Enter operator (+, -, *, /, %): ");
    io::stdout().flush().unwrap();
    let mut op = String::new();
    io::stdin().read_line(&mut op).unwrap();
    let op = op.trim();

    print!("Enter second number: ");
    io::stdout().flush().unwrap();
    let mut num2_str = String::new();
    io::stdin().read_line(&mut num2_str).unwrap();
    let num2: f64 = num2_str.trim().parse().unwrap_or(0.0);

    let result = match op {
        "+" => num1 + num2,
        "-" => num1 - num2,
        "*" => num1 * num2,
        "/" => {
            if num2 == 0.0 {
                println!("Error: Division by zero!");
                return;
            }
            num1 / num2
        }
        "%" => num1 % num2,
        _ => {
            println!("Invalid operator!");
            return;
        }
    };

    println!("Result: {} {} {} = {}", num1, op, num2, result);
}

fn scientific_functions() {
    println!("\n--- Scientific Functions ---");
    
    println!("1. Square root");
    println!("2. Power");
    println!("3. Sine");
    println!("4. Cosine");
    println!("5. Tangent");
    println!("6. Logarithm (base 10)");
    println!("7. Natural logarithm");
    print!("Choose a function: ");
    io::stdout().flush().unwrap();

    let mut choice = String::new();
    io::stdin().read_line(&mut choice).unwrap();
    let choice = choice.trim();

    print!("Enter number: ");
    io::stdout().flush().unwrap();
    let mut num_str = String::new();
    io::stdin().read_line(&mut num_str).unwrap();
    let num: f64 = num_str.trim().parse().unwrap_or(0.0);

    let result = match choice {
        "1" => {
            if num < 0.0 {
                println!("Error: Cannot calculate square root of negative number!");
                return;
            }
            num.sqrt()
        }
        "2" => {
            print!("Enter exponent: ");
            io::stdout().flush().unwrap();
            let mut exp_str = String::new();
            io::stdin().read_line(&mut exp_str).unwrap();
            let exp: f64 = exp_str.trim().parse().unwrap_or(0.0);
            num.powf(exp)
        }
        "3" => num.to_radians().sin(),
        "4" => num.to_radians().cos(),
        "5" => num.to_radians().tan(),
        "6" => {
            if num <= 0.0 {
                println!("Error: Logarithm undefined for non-positive numbers!");
                return;
            }
            num.log10()
        }
        "7" => {
            if num <= 0.0 {
                println!("Error: Natural logarithm undefined for non-positive numbers!");
                return;
            }
            num.ln()
        }
        _ => {
            println!("Invalid function!");
            return;
        }
    };

    let function_name = match choice {
        "1" => "sqrt",
        "2" => "pow",
        "3" => "sin",
        "4" => "cos",
        "5" => "tan",
        "6" => "log10",
        "7" => "ln",
        _ => "unknown",
    };

    println!("{}({}) = {}", function_name, num, result);
}

fn unit_conversion() {
    println!("\n--- Unit Conversion ---");
    
    println!("1. Celsius to Fahrenheit");
    println!("2. Fahrenheit to Celsius");
    println!("3. Meters to Feet");
    println!("4. Feet to Meters");
    println!("5. Kilograms to Pounds");
    println!("6. Pounds to Kilograms");
    print!("Choose conversion: ");
    io::stdout().flush().unwrap();

    let mut choice = String::new();
    io::stdin().read_line(&mut choice).unwrap();
    let choice = choice.trim();

    print!("Enter value: ");
    io::stdout().flush().unwrap();
    let mut value_str = String::new();
    io::stdin().read_line(&mut value_str).unwrap();
    let value: f64 = value_str.trim().parse().unwrap_or(0.0);

    let (from_unit, to_unit, result) = match choice {
        "1" => ("°C", "°F", value * 9.0 / 5.0 + 32.0),
        "2" => ("°F", "°C", (value - 32.0) * 5.0 / 9.0),
        "3" => ("m", "ft", value * 3.28084),
        "4" => ("ft", "m", value / 3.28084),
        "5" => ("kg", "lb", value * 2.20462),
        "6" => ("lb", "kg", value / 2.20462),
        _ => {
            println!("Invalid conversion!");
            return;
        }
    };

    println!("{} {} = {:.2} {}", value, from_unit, result, to_unit);
}

// Additional utility functions
fn factorial(n: u64) -> u64 {
    if n == 0 {
        1
    } else {
        n * factorial(n - 1)
    }
}

fn calculate_bmi(weight_kg: f64, height_m: f64) -> f64 {
    if height_m <= 0.0 {
        return 0.0;
    }
    weight_kg / (height_m * height_m)
}
