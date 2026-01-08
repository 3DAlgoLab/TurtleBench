import os
import subprocess
from svg_turtle import SvgTurtle
import cairosvg
from PIL import Image
import io


def transform_turtle_to_svg(code):
    """Transform regular turtle code to SVG turtle compatible code."""
    
    transformations = [
        # Remove turtle imports
        ('import turtle', '# import turtle'),
        ('from turtle import', '# from turtle import'),
        # Replace turtle.Turtle() assignments with just a comment
        ('t = turtle.Turtle()', '# t = turtle.Turtle()'),
        ('= turtle.Turtle()', '= turtle.Turtle()'),
        ('turtle.Turtle()', 'turtle.Turtle()'),
        # Replace turtle. calls with t.
        ('turtle.', 't.'),
        # Replace methods that don't exist in SVG turtle
        ('.done()', '# .done()'),
        ('.pensize(', '.width('),  # SVG turtle uses width()
    ]
    
    transformed = code
    for old, new in transformations:
        transformed = transformed.replace(old, new)
    
    return transformed


def execute_svg_code(code, save_path, task_name):
    """Execute SVG turtle code and save as PNG."""
    
    # Create complete SVG-ready code
    pre_code = """from svg_turtle import SvgTurtle
import cairosvg
import os

# Create SVG turtle instance
t = SvgTurtle(800, 600)

"""
    
    post_code = f"""

# Save SVG to PNG
svg_data = t.to_svg()
png_file = os.path.join("{save_path}", f"{task_name}.png")

# Convert SVG to PNG using cairosvg
try:
    cairosvg.svg2png(bytestring=svg_data, write_to=png_file, background_color="white")
    print(f"Successfully saved PNG to: {{png_file}}")
except Exception as e:
    print(f"Error converting SVG to PNG: {{e}}")

"""
    
    transformed_code = transform_turtle_to_svg(code)
    return pre_code + transformed_code + post_code


def code_to_image_svg(piece_of_code, task_name, save_path, remove_code_file=True):
    """Convert turtle code to image using SVG turtle."""
    
    try:
        # Transform the code for SVG compatibility
        svg_code = execute_svg_code(piece_of_code, save_path, task_name)
    except Exception as e:
        print(f"Error processing code: {e}, task: {task_name}")
        return False
    
    # Create temporary Python file to execute
    file_path = f"svg_file_path_{task_name}.py"
    with open(file_path, "w") as file:
        file.write(svg_code)
    
    try:
        # Execute the code using uv run
        completed_process = subprocess.run(
            ["uv", "run", "python", file_path], 
            timeout=20,
            capture_output=True,
            text=True
        )
        
        # Clean up temporary file
        if remove_code_file:
            os.remove(file_path)
        
        if completed_process.returncode == 0:
            # Check if PNG file was created
            png_file = os.path.join(save_path, f"{task_name}.png")
            if os.path.exists(png_file):
                return True
            else:
                print(f"PNG file not created for task {task_name}")
                return False
        else:
            print(f"Process failed for task {task_name}, return code: {completed_process.returncode}")
            print(f"Error output: {completed_process.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Process timed out for task {task_name}")
        if remove_code_file and os.path.exists(file_path):
            os.remove(file_path)
        return False
    except Exception as e:
        print(f"Exception during execution for task {task_name}: {e}")
        if remove_code_file and os.path.exists(file_path):
            os.remove(file_path)
        return False


# Import original functions for fallback
from utils.code_analysis import insert_pensize_and_hideturtle, find_screen_variable_name
from utils.sandbox import execute_combined_code


def code_to_image(piece_of_code, task_name, save_path, remove_code_file=False):
    """Main function - try SVG turtle first, fallback to original turtle."""    
    return code_to_image_svg(piece_of_code, task_name, save_path, remove_code_file)
    
    