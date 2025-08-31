#!/usr/bin/env python3
"""
ASCII Art Generator
Creates various ASCII art patterns and designs
"""

import random
import time

def create_pyramid(height):
    """Create a pyramid ASCII art"""
    print("Pyramid:")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(f"{spaces}{stars}")

def create_diamond(size):
    """Create a diamond ASCII art"""
    print("Diamond:")
    # Upper half
    for i in range(1, size + 1):
        spaces = " " * (size - i)
        stars = "*" * (2 * i - 1)
        print(f"{spaces}{stars}")
    
    # Lower half
    for i in range(size - 1, 0, -1):
        spaces = " " * (size - i)
        stars = "*" * (2 * i - 1)
        print(f"{spaces}{stars}")

def create_heart():
    """Create a heart ASCII art"""
    print("Heart:")
    heart = [
        "  ***   ***  ",
        " ***** ***** ",
        "*************",
        " *********** ",
        "  *********  ",
        "   *******   ",
        "    *****    ",
        "     ***     ",
        "      *      "
    ]
    for line in heart:
        print(line)

def create_tree(height):
    """Create a Christmas tree ASCII art"""
    print("Christmas Tree:")
    for i in range(1, height + 1):
        spaces = " " * (height - i)
        stars = "*" * (2 * i - 1)
        print(f"{spaces}{stars}")
    
    # Trunk
    trunk_spaces = " " * (height - 2)
    print(f"{trunk_spaces}***")
    print(f"{trunk_spaces}***")

def create_animated_spinner():
    """Create an animated spinner"""
    print("Animated Spinner:")
    spinner_chars = ["|", "/", "-", "\\"]
    for i in range(20):
        print(f"\r{spinner_chars[i % 4]} Loading...", end="", flush=True)
        time.sleep(0.1)
    print("\rDone!          ")

def create_text_art(text):
    """Create ASCII art from text"""
    print(f"Text Art: {text}")
    art = f"""
  ____  _  _  ____  ____  
 / ___)( \\/ )/ ___)(_  _) 
 \\___ \\ )  / \\___ \\  )(  
 (____/(__/  (____/ (__)  
    """
    print(art)

def main():
    """Main function to demonstrate ASCII art"""
    print("=" * 50)
    print("ASCII ART GENERATOR")
    print("=" * 50)
    
    # Generate different ASCII art
    create_pyramid(5)
    print()
    
    create_diamond(4)
    print()
    
    create_heart()
    print()
    
    create_tree(6)
    print()
    
    create_text_art("PYTHON")
    print()
    
    create_animated_spinner()
    print()

if __name__ == "__main__":
    main()
