# Web Server

A simple web server written in Rust that serves HTML pages.

## Features

- Handles HTTP GET requests
- Serves a home page and a 404 error page
- Basic routing functionality

## Usage

```bash
# Build the project
cargo build

# Run the server
cargo run

# Access the server in your browser
http://127.0.0.1:7878
```

## Project Structure

```
web-server/
├── Cargo.toml
├── src/
│   └── main.rs
├── hello.html
└── 404.html
```

## Dependencies

This project uses only the Rust standard library - no external dependencies.

## Contributing

Feel free to contribute by submitting pull requests or creating issues.

## License

This project is open source and available under the MIT License.
