#!/usr/bin/env python3
"""
Simple CSS Art Generator
Creates basic CSS art files
"""

import os
from datetime import datetime

def create_simple_art():
    """Create a simple CSS art (smiley face)"""
    css = """
/* Simple CSS Art - Smiley Face */
.art-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.smiley {
    width: 200px;
    height: 200px;
    background: #FFD700;
    border-radius: 50%;
    position: relative;
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

.eye {
    width: 30px;
    height: 30px;
    background: #333;
    border-radius: 50%;
    position: absolute;
}

.eye-left {
    top: 60px;
    left: 50px;
}

.eye-right {
    top: 60px;
    right: 50px;
}

.mouth {
    width: 100px;
    height: 50px;
    border-bottom: 10px solid #333;
    border-radius: 0 0 50px 50px;
    position: absolute;
    bottom: 40px;
    left: 50px;
}
"""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Art - Smiley Face</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="art-container">
        <div class="smiley">
            <div class="eye eye-left"></div>
            <div class="eye eye-right"></div>
            <div class="mouth"></div>
        </div>
    </div>
</body>
</html>"""
    
    return html

def save_html(content, filename):
    """Save HTML content to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully created: {filename}")
        return True
    except Exception as e:
        print(f"Error creating {filename}: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("SIMPLE CSS ART GENERATOR")
    print("=" * 50)
    
    # Create simple art
    html_content = create_simple_art()
    filename = "simple_smiley.html"
    
    if save_html(html_content, filename):
        print(f"\nCSS art file '{filename}' has been created successfully!")
        print("Open it in a web browser to see the smiley face.")
    else:
        print("\nFailed to create CSS art file.")

if __name__ == "__main__":
    main()
