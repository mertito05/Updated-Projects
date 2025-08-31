#!/usr/bin/env python3
"""
CSS Art Generator
Creates CSS-based art and animations
"""

import os
import random
from datetime import datetime

def generate_css_art(art_type="simple"):
    print(f"Generating CSS art of type: {art_type}")  # Debugging line
    """Generate different types of CSS art"""
    
    if art_type == "simple":
        return generate_simple_art()
    elif art_type == "animated":
        return generate_animated_art()
    elif art_type == "geometric":
        return generate_geometric_art()
    else:
        return generate_simple_art()

def generate_simple_art():
    """Generate simple CSS art (smiley face)"""
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
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Art - Smiley Face</title>
    <style>
        {{CSS_CONTENT}}
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
</html>
""".replace("{{CSS_CONTENT}}", css)
    
    return html

def generate_animated_art():
    """Generate animated CSS art (pulsing circles)"""
    css = """
/* Animated CSS Art - Pulsing Circles */
.art-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #1a1a1a;
    overflow: hidden;
}

.circle {
    position: absolute;
    border-radius: 50%;
    animation: pulse 2s infinite ease-in-out;
}

.circle-1 {
    width: 100px;
    height: 100px;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    animation-delay: 0s;
}

.circle-2 {
    width: 150px;
    height: 150px;
    background: linear-gradient(45deg, #45b7d1, #96ceb4);
    animation-delay: 0.5s;
}

.circle-3 {
    width: 200px;
    height: 200px;
    background: linear-gradient(45deg, #f093fb, #f5576c);
    animation-delay: 1s;
}

.circle-4 {
    width: 250px;
    height: 250px;
    background: linear-gradient(45deg, #4facfe, #00f2fe);
    animation-delay: 1.5s;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
        opacity: 0.7;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
}
"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Art - Animated Circles</title>
    <style>
        {{CSS_CONTENT}}
    </style>
</head>
<body>
    <div class="art-container">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
        <div class="circle circle-4"></div>
    </div>
</body>
</html>
""".replace("{{CSS_CONTENT}}", css)
    
    return html

def generate_geometric_art():
    """Generate geometric CSS art"""
    css = """
/* Geometric CSS Art */
.art-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #2c3e50;
    perspective: 1000px;
}

.geometric-shapes {
    position: relative;
    transform-style: preserve-3d;
    animation: rotate 10s infinite linear;
}

.triangle {
    width: 0;
    height: 0;
    border-left: 50px solid transparent;
    border-right: 50px solid transparent;
    border-bottom: 100px solid #e74c3c;
    position: absolute;
    animation: float 3s infinite ease-in-out;
}

.square {
    width: 80px;
    height: 80px;
    background: #3498db;
    position: absolute;
    animation: float 4s infinite ease-in-out reverse;
}

.circle {
    width: 60px;
    height: 60px;
    background: #9b59b6;
    border-radius: 50%;
    position: absolute;
    animation: float 5s infinite ease-in-out;
}

@keyframes rotate {
    from { transform: rotateY(0deg); }
    to { transform: rotateY(360deg); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Art - Geometric Shapes</title>
    <style>
        {{CSS_CONTENT}}
    </style>
</head>
<body>
    <div class="art-container">
        <div class="geometric-shapes">
            <div class="triangle" style="top: -50px; left: -25px;"></div>
            <div class="square" style="top: 30px; left: 60px;"></div>
            <div class="circle" style="top: -20px; left: 120px;"></div>
        </div>
    </div>
</body>
</html>
""".replace("{{CSS_CONTENT}}", css)
    
    return html

def save_css_art(html_content, filename=None):
    """Save CSS art to HTML file"""
    print("Saving CSS art...")
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"css_art_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Saved CSS art as: {filename}")
    print(f"Saved CSS art as: {filename}")  # Debugging line
    return filename

def main():
    """Main function to demonstrate CSS art generation"""
    print("=" * 50)
    print("CSS ART GENERATOR")
    print("=" * 50)
    
    # Generate different types of CSS art
    art_types = ["simple", "animated", "geometric"]
    
    for art_type in art_types:
        print(f"\nGenerating {art_type} CSS art...")
        html_content = generate_css_art(art_type)
        filename = save_css_art(html_content, f"{art_type}_art.html")
        print(f"Saved as: {filename}")
    
    print(f"\nAll CSS art files have been generated in the current directory!")
    print("Open them in a web browser to see the artwork.")

if __name__ == "__main__":
    main()
