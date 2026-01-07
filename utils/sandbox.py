import os


# Function to combine and execute the entire code
def execute_combined_code(code, screen_variable_name, save_path, task_name):
    post_code_address = "utils/post_code.txt"
    post_code_with_screen_address = "utils/post_code_with_screen_name.txt"
    pre_json_code = """import subprocess\nimport os\nfrom math import *\nimport utils.rabbit as rabbit\n\n"""
    # tracer should be called after screen creation
    if screen_variable_name:
        post_json_code = open(post_code_with_screen_address, "r").read()
    else:
        post_json_code = open(post_code_address, "r").read()
    post_json_code = post_json_code.format(
        SAVE_DIR=save_path,
        task_name=task_name,
        screen_variable_name=screen_variable_name,
    )
    # Combine the code segments
    combined_code = pre_json_code + (code if code else "") + post_json_code
    return combined_code
