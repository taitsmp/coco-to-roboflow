#!/usr/bin/env python3

from PIL import Image, ImageDraw
import os

def create_test_image(filename, width, height, color):
    """Create a simple test image with a colored rectangle"""
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a colored rectangle
    draw.rectangle([100, 100, 300, 300], fill=color)
    
    img.save(filename)
    print(f"Created test image: {filename}")

def main():
    # Create output directory if it doesn't exist
    os.makedirs('test_data/images', exist_ok=True)
    
    # Create test images
    create_test_image('test_data/images/image1.jpg', 640, 480, 'red')
    create_test_image('test_data/images/image2.jpg', 640, 480, 'blue')

if __name__ == '__main__':
    main()
