use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};

fn main() {
    println!("Data Processor - Processing sample data");
    
    // Sample data processing
    let data = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    // Calculate statistics
    let sum: i32 = data.iter().sum();
    let avg = sum as f64 / data.len() as f64;
    let max = *data.iter().max().unwrap();
    let min = *data.iter().min().unwrap();
    
    println!("Data: {:?}", data);
    println!("Sum: {}", sum);
    println!("Average: {:.2}", avg);
    println!("Max: {}", max);
    println!("Min: {}", min);
    
    // Word frequency counter
    let text = "hello world hello rust programming world";
    let word_counts = count_words(text);
    println!("\nWord frequencies: {:?}", word_counts);
    
    // File operations
    if let Err(e) = write_sample_data() {
        eprintln!("Error writing file: {}", e);
    }
    
    if let Err(e) = read_sample_data() {
        eprintln!("Error reading file: {}", e);
    }
}

fn count_words(text: &str) -> HashMap<String, u32> {
    let mut counts = HashMap::new();
    
    for word in text.split_whitespace() {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }
    
    counts
}

fn write_sample_data() -> io::Result<()> {
    let mut file = File::create("sample_data.txt")?;
    writeln!(file, "Name,Age,Score")?;
    writeln!(file, "Alice,25,95")?;
    writeln!(file, "Bob,30,88")?;
    writeln!(file, "Charlie,22,92")?;
    println!("\nSample data written to sample_data.txt");
    Ok(())
}

fn read_sample_data() -> io::Result<()> {
    let file = File::open("sample_data.txt")?;
    let reader = BufReader::new(file);
    
    println!("\nReading sample data:");
    for line in reader.lines() {
        println!("{}", line?);
    }
    
    Ok(())
}
