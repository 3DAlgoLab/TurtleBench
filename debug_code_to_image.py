#!/usr/bin/env python3
"""
Test to debug why code_to_image fails but direct turtle works
"""

import os
import subprocess
import tempfile
import time

def test_direct_subprocess():
    """Test direct subprocess call like code_to_image does."""
    print("=== Testing Direct Subprocess (like code_to_image) ===")
    
    # Simple turtle code
    code = '''import turtle
import os
os.environ['DISPLAY'] = ':99'  # Try to set display in code
t = turtle.Turtle()
t.forward(100)
turtle.done()'''
    
    # Write to file like code_to_image does
    file_path = "test_subprocess.py"
    with open(file_path, "w") as f:
        f.write(code)
    
    try:
        # Test 1: System Python (like current code_to_image)
        print("1. Testing system Python...")
        result1 = subprocess.run(["python", file_path], 
                              capture_output=True, text=True, timeout=10)
        print(f"   System Python - Exit: {result1.returncode}")
        print(f"   Stdout: {result1.stdout}")
        print(f"   Stderr: {result1.stderr}")
        
        # Test 2: UV Python (what we want)
        print("2. Testing uv run Python...")
        result2 = subprocess.run(["uv", "run", "python", file_path], 
                              capture_output=True, text=True, timeout=10)
        print(f"   UV Python - Exit: {result2.returncode}")
        print(f"   Stdout: {result2.stdout}")
        print(f"   Stderr: {result2.stderr}")
        
        # Test 3: System Python with DISPLAY env
        print("3. Testing system Python with DISPLAY=:99...")
        env = os.environ.copy()
        env['DISPLAY'] = ':99'
        result3 = subprocess.run(["python", file_path], 
                              env=env, capture_output=True, text=True, timeout=10)
        print(f"   System Python+DISPLAY - Exit: {result3.returncode}")
        print(f"   Stdout: {result3.stdout}")
        print(f"   Stderr: {result3.stderr}")
        
    except subprocess.TimeoutExpired:
        print("   Subprocess timed out (common issue!)")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def test_modified_code_to_image():
    """Test code_to_image with subprocess fix."""
    print("\n=== Testing Modified code_to_image ===")
    
    # Temporarily modify code_to_image to use uv run
    original_code = '''
def code_to_image(piece_of_code, task_name, save_path):
    try:
        clean_code = insert_pensize_and_hideturtle(piece_of_code)
    except Exception as e:
        print(e, task_name)
        clean_code = ""
        return False
    try:
        svn = find_screen_variable_name(clean_code)
    except Exception:
        print("error on code:", f"{task_name}.txt")
        return False
    code = execute_combined_code(
        clean_code, screen_variable_name=svn, task_name=task_name, save_path=save_path
    )
    file_path = f"file_path_{task_name}.py"
    with open(file_path, "w") as file:
        file.write(code)
    # MODIFIED: Use uv run instead of python
    completed_process = subprocess.run(["uv", "run", "python", file_path])
    if completed_process.returncode == 0:
        os.remove(file_path)
        return True
    else:
        print("Process failed, return code:", completed_process.returncode)
        return False
'''
    
    with open("test_code_to_image.py", "w") as f:
        f.write(original_code + '''
    
import sys
import subprocess
import os
sys.path.insert(0, ".")
from utils.code_analysis import insert_pensize_and_hideturtle
from utils.code_analysis import find_screen_variable_name
from utils.sandbox import execute_combined_code

# Test the function
test_code = """import turtle
t = turtle.Turtle()
t.forward(100)
t.right(90)
t.forward(50)
turtle.done()"""

result = code_to_image(test_code, "test_modified", ".")
print(f"Modified code_to_image result: {result}")
''')
    
    try:
        env = os.environ.copy()
        env['DISPLAY'] = ':99'
        
        result = subprocess.run(["uv", "run", "python", "test_code_to_image.py"], 
                              env=env, capture_output=True, text=True, timeout=15)
        print(f"Modified test - Exit: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
    except subprocess.TimeoutExpired:
        print("Modified test also timed out!")
    
    finally:
        for f in ["test_code_to_image.py", "file_path_test_modified.py"]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    print("Debugging code_to_image timeout issues...")
    test_direct_subprocess()
    test_modified_code_to_image()