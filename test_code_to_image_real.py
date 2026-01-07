import os
import tempfile
import shutil
import subprocess
import pytest
from pathlib import Path

# Set up virtual display for SSH environments
os.environ['DISPLAY'] = ':99'

from utils.code_to_image import code_to_image


@pytest.fixture
def real_test_setup():
    """Set up test fixtures for real image rendering."""
    test_dir = tempfile.mkdtemp()
    task_name = "real_test"
    save_path = test_dir
    
    # Simple valid turtle code that should work
    simple_code = """import turtle
t = turtle.Turtle()
t.forward(100)
t.right(90)
t.forward(50)
turtle.done()"""

    # More complex turtle code
    complex_code = """import turtle
screen = turtle.Screen()
t = turtle.Turtle()
t.speed(5)
for i in range(4):
    t.forward(100)
    t.right(90)
t.penup()
t.goto(50, 50)
t.pendown()
t.circle(50)
turtle.done()"""
    
    yield test_dir, task_name, save_path, simple_code, complex_code
    
    # Cleanup after each test
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_real_image_generation_simple(real_test_setup):
    """Test real image generation with xvfb for simple turtle code."""
    test_dir, task_name, save_path, simple_code, complex_code = real_test_setup
    
    # Use xvfb-run to execute the code_to_image function in a virtual display
    script = f'''
import sys
sys.path.insert(0, "{os.getcwd()}")
import os
os.environ['DISPLAY'] = ':99'
from utils.code_to_image import code_to_image

result = code_to_image("""{simple_code}""", "{task_name}_simple", "{save_path}")
print(f"Result: {{result}}")

# Check if image was created
import os
image_path = os.path.join("{save_path}", "{task_name}_simple.jpg")
print(f"Image exists: {{os.path.exists(image_path)}}")
if os.path.exists(image_path):
    print(f"Image size: {{os.path.getsize(image_path)}} bytes")
'''
    
    try:
        # Run the test script with xvfb
        result = subprocess.run(
            ['xvfb-run', '-a', 'python', '-c', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("Script output:", result.stdout)
        print("Script errors:", result.stderr)
        
        # Check if the execution was successful
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check if image was actually created
        image_path = os.path.join(save_path, f"{task_name}_simple.jpg")
        assert os.path.exists(image_path), f"Image not found at {image_path}"
        assert os.path.getsize(image_path) > 0, "Image file is empty"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Image generation timed out")
    except Exception as e:
        pytest.fail(f"Real image generation failed: {e}")


def test_real_image_generation_complex(real_test_setup):
    """Test real image generation with xvfb for complex turtle code."""
    test_dir, task_name, save_path, simple_code, complex_code = real_test_setup
    
    script = f'''
import sys
sys.path.insert(0, "{os.getcwd()}")
import os
os.environ['DISPLAY'] = ':99'
from utils.code_to_image import code_to_image

result = code_to_image("""{complex_code}""", "{task_name}_complex", "{save_path}")
print(f"Result: {{result}}")

# Check if image was created
import os
image_path = os.path.join("{save_path}", "{task_name}_complex.jpg")
print(f"Image exists: {{os.path.exists(image_path)}}")
if os.path.exists(image_path):
    print(f"Image size: {{os.path.getsize(image_path)}} bytes")
'''
    
    try:
        # Run the test script with xvfb
        result = subprocess.run(
            ['xvfb-run', '-a', 'python', '-c', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("Script output:", result.stdout)
        print("Script errors:", result.stderr)
        
        # Check if the execution was successful
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check if image was actually created
        image_path = os.path.join(save_path, f"{task_name}_complex.jpg")
        assert os.path.exists(image_path), f"Image not found at {image_path}"
        assert os.path.getsize(image_path) > 0, "Image file is empty"
        
    except subprocess.TimeoutExpired:
        pytest.fail("Complex image generation timed out")
    except Exception as e:
        pytest.fail(f"Complex image generation failed: {e}")


def test_image_quality_and_properties(real_test_setup):
    """Test that generated images have reasonable properties."""
    test_dir, task_name, save_path, simple_code, complex_code = real_test_setup
    
    # First generate an image
    script = f'''
import sys
sys.path.insert(0, "{os.getcwd()}")
import os
os.environ['DISPLAY'] = ':99'
from utils.code_to_image import code_to_image

result = code_to_image("""{simple_code}""", "{task_name}_quality", "{save_path}")
'''
    
    try:
        result = subprocess.run(
            ['xvfb-run', '-a', 'python', '-c', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check image properties
        image_path = os.path.join(save_path, f"{task_name}_quality.jpg")
        assert os.path.exists(image_path), f"Image not found at {image_path}"
        
        # Check file size (should be reasonable for a turtle drawing)
        file_size = os.path.getsize(image_path)
        assert file_size > 100, f"Image too small: {file_size} bytes"
        assert file_size < 5_000_000, f"Image too large: {file_size} bytes"  # Less than 5MB
        
        # Try to read the image with PIL to verify it's a valid JPEG
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                assert img.format == 'JPEG', f"Image format is not JPEG: {img.format}"
                assert img.size[0] > 0 and img.size[1] > 0, f"Invalid image dimensions: {img.size}"
                print(f"Image dimensions: {img.size}")
        except ImportError:
            # PIL is not available, but we at least know the file exists and has content
            print("PIL not available, skipping detailed image validation")
        
    except subprocess.TimeoutExpired:
        pytest.fail("Image generation timed out")
    except Exception as e:
        pytest.fail(f"Image quality test failed: {e}")


def test_direct_xvfb_functionality():
    """Test that xvfb is working correctly in this environment."""
    # Simple test to verify xvfb is working
    test_script = '''
import os
os.environ['DISPLAY'] = ':99'
import turtle

# Try to create a simple turtle drawing without actually saving
screen = turtle.Screen()
t = turtle.Turtle()
t.forward(100)
screen.bye()
print("Xvfb turtle test successful")
'''
    
    try:
        result = subprocess.run(
            ['xvfb-run', '-a', 'python', '-c', test_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0, f"Xvfb test failed: {result.stderr}"
        assert "Xvfb turtle test successful" in result.stdout
        
    except subprocess.TimeoutExpired:
        pytest.fail("Xvfb functionality test timed out")
    except Exception as e:
        pytest.fail(f"Xvfb functionality test failed: {e}")