# Markdown to HTML Converter

A simple console-based Markdown to HTML converter implemented in C that converts basic Markdown syntax to HTML.

## Features

- Convert Markdown headings to HTML
- Convert bold and italic text
- Convert code blocks
- Convert links and images
- Basic paragraph handling

## Usage

1. Compile the program:
   ```bash
   gcc main.c -o markdown_converter
   ```

2. Run the executable:
   ```bash
   ./markdown_converter
   ```

## Supported Markdown Syntax

- Headers: `# Header 1`, `## Header 2`, etc.
- Bold: `**bold text**`
- Italic: `*italic text*`
- Code: ```code```
- Links: `[text](url)`
- Images: `![alt text](image_url)`

## Future Enhancements

- Support for nested formatting
- File input/output support
- More Markdown features (tables, lists, etc.)
- Command-line arguments for file processing
