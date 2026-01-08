from utils.code_analysis import *
import os
import subprocess

from utils.sandbox import execute_combined_code
from utils.code_to_image_svg import code_to_image_svg


def code_to_image(piece_of_code, task_name, save_path):
    """Main function - try SVG turtle first, fallback to original turtle."""
    
    # Try SVG turtle first (headless compatible)
    if code_to_image_svg(piece_of_code, task_name, save_path):
        return True
    
    # Fallback to original turtle if SVG fails
    print(f"SVG turtle failed for task {task_name}, trying original turtle")
    try:
        clean_code = insert_pensize_and_hideturtle(piece_of_code)
    except Exception as e:
        print(e, task_name)
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
        file.write(code if code else "")
    
    # Ensure environment variables are passed to subprocess
    env = os.environ.copy()
    if 'DISPLAY' not in env:
        env['DISPLAY'] = ':99'
    
    # Use uv run and pass environment
    completed_process = subprocess.run(
        ["uv", "run", "python", file_path], 
        env=env,
        timeout=20  # Add timeout to prevent hanging
    )
    if completed_process.returncode == 0:
        os.remove(file_path)
        return True
    else:
        print("Process failed, return code:", completed_process.returncode)
        return False
