#!/usr/bin/env python3
"""
Generate real turtle image in SSH environment and save it permanently.
This shows exactly where images are saved.
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

def setup_xvfb_and_generate_image():
    """Set up Xvfb and generate a real turtle image."""
    
    print("Setting up Xvfb for real turtle graphics...")
    
    # Kill any existing Xvfb on display :101
    subprocess.run(['killall', 'Xvfb'], capture_output=True)
    
    # Start Xvfb with proper settings
    xvfb_process = subprocess.Popen([
        'Xvfb', ':101', '-ac', '-screen', '0', '1024x768x24',
        '+extension', 'GLX', '+render', '-noreset'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Give Xvfb time to start
    time.sleep(2)
    
    try:
        # Set environment for turtle
        env = os.environ.copy()
        env['DISPLAY'] = ':101'
        
        # Create turtle drawing code
        turtle_code = '''
import turtle
import os

print("Creating turtle graphics...")
os.environ['DISPLAY'] = ':101'

# Create screen and turtle
screen = turtle.Screen()
screen.title("Real Turtle Graphics in SSH")
t = turtle.Turtle()

# Draw a colorful pattern
t.speed(5)
colors = ['red', 'blue', 'green', 'orange', 'purple']

for i in range(5):
    t.color(colors[i % len(colors)])
    t.pensize(3)
    t.forward(100)
    t.right(72)
    t.forward(50)
    t.left(144)

t.color('black')
t.penup()
t.goto(0, -150)
t.write("Real Image Generated in SSH!", align="center", font=("Arial", 16, "bold"))

# Save to PostScript
canvas = screen.getcanvas()
ps_file = 'real_turtle_image.ps'
canvas.postscript(file=ps_file, colormode='color')
print(f"PostScript saved to: {os.path.abspath(ps_file)}")

# Close turtle
screen.bye()
print("Turtle graphics completed successfully!")
'''
        
        # Write to temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(turtle_code)
            script_path = f.name
        
        try:
            print("Running turtle graphics with Xvfb...")
            result = subprocess.run([
                'uv', 'run', 'python', script_path
            ], env=env, capture_output=True, text=True, timeout=20)
            
            print("Turtle execution output:")
            print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            if result.returncode == 0:
                # Convert PostScript to JPEG if PIL is available
                ps_file = 'real_turtle_image.ps'
                if os.path.exists(ps_file):
                    ps_size = os.path.getsize(ps_file)
                    print(f"\n✅ PostScript file created:")
                    print(f"   Path: {os.path.abspath(ps_file)}")
                    print(f"   Size: {ps_size} bytes")
                    
                    try:
                        from PIL import Image
                        
                        # Open PostScript and convert to JPEG
                        img = Image.open(ps_file)
                        jpg_file = 'real_turtle_image.jpg'
                        img.save(jpg_file, 'JPEG', quality=95)
                        
                        jpg_size = os.path.getsize(jpg_file)
                        print(f"\n✅ JPEG image created:")
                        print(f"   Path: {os.path.abspath(jpg_file)}")
                        print(f"   Size: {jpg_size} bytes")
                        
                        return jpg_file
                        
                    except ImportError:
                        print(f"\n📁 PostScript file available (PIL not installed for JPEG conversion)")
                        print(f"   You can view this file with PostScript viewers")
                        return ps_file
                        
                else:
                    print("❌ No PostScript file was created")
            else:
                print(f"❌ Turtle execution failed with code: {result.returncode}")
                
        finally:
            # Clean up temporary script
            if os.path.exists(script_path):
                os.remove(script_path)
    
    finally:
        # Clean up Xvfb
        xvfb_process.terminate()
        try:
            xvfb_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            xvfb_process.kill()
    
    return None

def generate_with_code_to_image():
    """Test the actual code_to_image function from TurtleBench."""
    
    print("\n" + "="*60)
    print("Testing utils.code_to_image function...")
    
    # Set up Xvfb
    subprocess.run(['killall', 'Xvfb'], capture_output=True)
    xvfb_process = subprocess.Popen([
        'Xvfb', ':102', '-ac', '-screen', '0', '1024x768x24',
        '+extension', 'GLX', '+render', '-noreset'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(2)
    
    try:
        # Create a simple output directory
        output_dir = "real_turtle_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create test script that uses code_to_image
        test_script = f'''
import sys
sys.path.insert(0, "{os.getcwd()}")
import os
os.environ['DISPLAY'] = ':102'

from utils.code_to_image import code_to_image

# Simple turtle code
code = """import turtle
t = turtle.Turtle()
t.speed(5)
t.pensize(3)
t.color('blue')
for i in range(4):
    t.forward(100)
    t.right(90)
turtle.done()"""

print("Using code_to_image function...")
result = code_to_image(code, "real_example", "{output_dir}")
print(f"code_to_image result: {{result}}")

# Check for generated image
import os
image_path = os.path.join("{output_dir}", "real_example.jpg")
if os.path.exists(image_path):
    print(f"✅ Image found at: {{os.path.abspath(image_path)}}")
    print(f"   Size: {{os.path.getsize(image_path)}} bytes")
else:
    print("❌ No image generated by code_to_image")
'''
        
        env = os.environ.copy()
        env['DISPLAY'] = ':102'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_script)
            script_path = f.name
        
        try:
            print("Running code_to_image test...")
            result = subprocess.run([
                'uv', 'run', 'python', script_path
            ], env=env, capture_output=True, text=True, timeout=30)
            
            print("code_to_image execution:")
            print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            # Check if image was created
            image_path = os.path.join(output_dir, "real_example.jpg")
            if os.path.exists(image_path):
                print(f"\n✅ SUCCESS: code_to_image generated image!")
                print(f"   Path: {os.path.abspath(image_path)}")
                return image_path
            else:
                print("❌ code_to_image did not generate image")
        
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)
    
    finally:
        xvfb_process.terminate()
        try:
            xvfb_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            xvfb_process.kill()
    
    return None

if __name__ == '__main__':
    print("Real Turtle Image Generation in SSH Environment")
    print("="*60)
    
    # Method 1: Direct turtle graphics
    image1 = setup_xvfb_and_generate_image()
    
    # Method 2: Using code_to_image function
    image2 = generate_with_code_to_image()
    
    print("\n" + "="*60)
    print("FINAL RESULTS:")
    print("="*60)
    
    if image1 and os.path.exists(image1):
        print(f"✅ Real turtle image #1: {os.path.abspath(image1)}")
    
    if image2 and os.path.exists(image2):
        print(f"✅ Real turtle image #2: {os.path.abspath(image2)}")
    
    if not (image1 or image2):
        print("❌ No images were generated")
    else:
        print(f"\n📁 Images are saved in: {os.path.abspath('.')}")
        print(f"📁 code_to_image outputs are in: {os.path.abspath('real_turtle_output')}")
        print("\nYou can view these images with any image viewer!")