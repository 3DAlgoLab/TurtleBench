#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from eval_dspy import eval_dspy

# Test DSPy evaluation with minimal parameters
print("Testing DSPy evaluation...")
try:
    MODEL_ID = "lm_studio/zai-org/glm-4.6v-flash"
    eval_dspy(
        model_name=MODEL_ID,
        task_type="scratch",
        modalities="text_only",
        prompting_mode="cot",
        save_responses=True,
    )
    print("DSPy evaluation completed successfully!")
except Exception as e:
    print(f"Error during DSPy evaluation: {e}")
    import traceback

    traceback.print_exc()
