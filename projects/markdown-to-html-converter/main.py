import re
import os

def markdown_to_html(markdown_text):
    """Convert Markdown text to HTML"""
    # Convert headers
    markdown_text = re.sub(r'^# (.*)$', r'<h1>\1</h1>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^## (.*)$', r'<h2>\1</h2>', markdown_text, flags=re.MULTILINE)
    markdown_text = re.sub(r'^### (.*)$', r'<h3>\1</h3>', markdown_text, flags=re.MULTILINE)
    
    # Convert bold text
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', markdown_text)
    markdown_text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', markdown_text)
    
    # Convert italic text
    markdown_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', r'<em>\1</em>', markdown_text)
    
    # Convert code blocks
    markdown_text = re.sub(r'`(.*?)`', r'<code>\1</code>', markdown_text)
    
    # Convert links
    markdown_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown_text)
    
    # Convert unordered lists
    lines = markdown_text.split('\n')
    in_list = False
    html_lines = []
    
    for line in lines:
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(line)
    
    if in_list:
        html_lines.append('</ul>')
    
    markdown_text = '\n'.join(html_lines)
    
    # Convert paragraphs
    paragraphs = markdown_text.split('\n\n')
    html_paragraphs = []
    
    for para in paragraphs:
        if para.strip() and not para.startswith('<') and not para.endswith('>'):
            html_paragraphs.append(f'<p>{para}</p>')
        else:
            html_paragraphs.append(para)
    
    return '\n\n'.join(html_paragraphs)

def convert_file(input_file, output_file):
    """Convert a Markdown file to HTML file"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        html_content = markdown_to_html(markdown_content)
        
        # Create HTML template
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Markdown</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        h1, h2, h3 {{
            color: #333;
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }}
        code {{
            background-color: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        ul {{
            background-color: #fff;
            padding: 15px 30px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"✅ Successfully converted {input_file} to {output_file}")
        
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} not found!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("Markdown to HTML Converter")
    print("==========================")
    
    while True:
        print("\nOptions:")
        print("1. Convert Markdown text")
        print("2. Convert Markdown file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\nEnter your Markdown text (press Ctrl+Z then Enter on Windows, or Ctrl+D on Unix to finish):")
            markdown_text = []
            try:
                while True:
                    line = input()
                    markdown_text.append(line)
            except EOFError:
                pass
            
            markdown_text = '\n'.join(markdown_text)
            html_output = markdown_to_html(markdown_text)
            
            print("\nHTML Output:")
            print("============")
            print(html_output)
            
            save_choice = input("\nSave to file? (y/n): ").strip().lower()
            if save_choice == 'y':
                filename = input("Enter filename (without extension): ").strip()
                if filename:
                    output_file = f"{filename}.html"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>Converted Markdown</title>\n</head>\n<body>\n{html_output}\n</body>\n</html>")
                    print(f"✅ Saved as {output_file}")
        
        elif choice == "2":
            input_file = input("Enter input Markdown file path: ").strip()
            if not input_file.endswith('.md'):
                input_file += '.md'
            
            output_file = input("Enter output HTML file name (without extension): ").strip()
            if not output_file:
                output_file = os.path.splitext(input_file)[0]
            output_file += '.html'
            
            convert_file(input_file, output_file)
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
