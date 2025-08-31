use std::fs;
use std::io::{self, Write};
use std::path::Path;

fn main() {
    println!("=== Image Processor ===");
    println!("Simple image metadata and basic processing tool");

    loop {
        println!("\nOptions:");
        println!("1. List image files in directory");
        println!("2. Get file information");
        println!("3. Create simple image (PPM format)");
        println!("4. Exit");
        print!("Choose an option: ");
        io::stdout().flush().unwrap();

        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim();

        match choice {
            "1" => list_image_files(),
            "2" => get_file_info(),
            "3" => create_simple_image(),
            "4" => {
                println!("Goodbye!");
                break;
            }
            _ => println!("Invalid option. Please try again."),
        }
    }
}

fn list_image_files() {
    println!("\n--- List Image Files ---");
    
    print!("Enter directory path: ");
    io::stdout().flush().unwrap();
    let mut dir_path = String::new();
    io::stdin().read_line(&mut dir_path).unwrap();
    let dir_path = dir_path.trim();

    if !Path::new(dir_path).exists() {
        println!("Directory not found: {}", dir_path);
        return;
    }

    let image_extensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ppm"];
    
    match fs::read_dir(dir_path) {
        Ok(entries) => {
            println!("\nImage files found:");
            let mut count = 0;
            
            for entry in entries {
                if let Ok(entry) = entry {
                    let path = entry.path();
                    if let Some(extension) = path.extension() {
                        if let Some(ext_str) = extension.to_str() {
                            if image_extensions.contains(&ext_str.to_lowercase().as_str()) {
                                if let Some(file_name) = path.file_name() {
                                    if let Some(name_str) = file_name.to_str() {
                                        println!("- {}", name_str);
                                        count += 1;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            if count == 0 {
                println!("No image files found in directory.");
            } else {
                println!("Total: {} image files", count);
            }
        }
        Err(e) => println!("Error reading directory: {}", e),
    }
}

fn get_file_info() {
    println!("\n--- Get File Information ---");
    
    print!("Enter file path: ");
    io::stdout().flush().unwrap();
    let mut file_path = String::new();
    io::stdin().read_line(&mut file_path).unwrap();
    let file_path = file_path.trim();

    if !Path::new(file_path).exists() {
        println!("File not found: {}", file_path);
        return;
    }

    match fs::metadata(file_path) {
        Ok(metadata) => {
            println!("\nFile Information:");
            println!("Path: {}", file_path);
            println!("Size: {} bytes", metadata.len());
            println!("Is file: {}", metadata.is_file());
            println!("Is directory: {}", metadata.is_dir());
            
            if let Ok(modified) = metadata.modified() {
                println!("Last modified: {:?}", modified);
            }
            
            if let Ok(created) = metadata.created() {
                println!("Created: {:?}", created);
            }
            
            if let Some(extension) = Path::new(file_path).extension() {
                if let Some(ext_str) = extension.to_str() {
                    println!("Extension: {}", ext_str);
                }
            }
        }
        Err(e) => println!("Error getting file information: {}", e),
    }
}

fn create_simple_image() {
    println!("\n--- Create Simple PPM Image ---");
    
    print!("Enter output file name (e.g., image.ppm): ");
    io::stdout().flush().unwrap();
    let mut file_name = String::new();
    io::stdin().read_line(&mut file_name).unwrap();
    let file_name = file_name.trim();

    print!("Enter width: ");
    io::stdout().flush().unwrap();
    let mut width_str = String::new();
    io::stdin().read_line(&mut width_str).unwrap();
    let width: usize = width_str.trim().parse().unwrap_or(100);

    print!("Enter height: ");
    io::stdout().flush().unwrap();
    let mut height_str = String::new();
    io::stdin().read_line(&mut height_str).unwrap();
    let height: usize = height_str.trim().parse().unwrap_or(100);

    // Create a simple gradient PPM image
    let mut ppm_content = String::new();
    ppm_content.push_str("P3\n");
    ppm_content.push_str(&format!("{} {}\n", width, height));
    ppm_content.push_str("255\n");

    for y in 0..height {
        for x in 0..width {
            let r = (x as f32 / width as f32 * 255.0) as u8;
            let g = (y as f32 / height as f32 * 255.0) as u8;
            let b = ((x + y) as f32 / (width + height) as f32 * 255.0) as u8;
            
            ppm_content.push_str(&format!("{} {} {} ", r, g, b));
        }
        ppm_content.push('\n');
    }

    match fs::write(file_name, ppm_content) {
        Ok(_) => println!("PPM image created successfully: {}", file_name),
        Err(e) => println!("Error creating image: {}", e),
    }
}
