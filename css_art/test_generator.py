#!/usr/bin/env python3
"""
Simple test script for CSS art generator
"""

import os
import sys

# Add the current directory to the path so we can import css_art_generator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import css_art_generator
    print("Successfully imported css_art_generator")
    
    # Test generating simple art
    print("Testing simple art generation...")
    html_content = css_art_generator.generate_simple_art()
    print(f"Generated HTML content length: {len(html_content)} characters")
    
    # Test saving
    print("Testing file saving...")
    filename = css_art_generator.save_css_art(html_content, "test_simple_art.html")
    print(f"File saved as: {filename}")
    
    # Check if file exists
    if os.path.exists(filename):
        print(f"File {filename} exists!")
        with open(filename, 'r') as f:
            content = f.read()
            print(f"File content length: {len(content)} characters")
    else:
        print(f"File {filename} does not exist!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
