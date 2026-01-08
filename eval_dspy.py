import json
import os
import argparse
import datetime
from tqdm import tqdm
from calculate_score import update_report
from prompts import system_prompts, user_prompts, user_prompt_final_piece
from utils.shape_similarity import calculate_accuracy
from utils.code_to_image import code_to_image
from utils.temp_directory import TempDirManager
from utils.watermark import watermark_and_save
from utils.code_preprocess import preprocess_response
from dotenv import load_dotenv

import dspy


class TurtleBenchDSPyAgent(dspy.Module):
    """DSPy agent for turtle code generation and evaluation."""

    def __init__(self, model_name="gpt4-v"):
        super().__init__()
        self.model_name = model_name

        # Initialize DSPy with GPT model
        load_dotenv()        
        self.lm = dspy.LM(model=model_name)
        
        # Configure DSPy
        dspy.configure(lm=self.lm)

        # Simple predictor for code generation
        self.predictor = dspy.ChainOfThought(
            "system_prompt, task_description, base_code, query, variables -> turtle_code"
        )

    def forward(self, task, task_type, task_mode, modalities, prompting_mode):
        """Process a single turtle task using DSPy."""

        try:
            # Get system prompt
            if task_type == "scratch":
                system_prompt = system_prompts[prompting_mode]["scratch"][modalities]
            elif task_type == "tweak":
                system_prompt = system_prompts[prompting_mode]["tweak"][task_mode][
                    modalities
                ]
            else:
                raise ValueError(f"Unsupported task_type: {task_type}")

            # Get user prompt
            user_prompt = ""
            if task_type == "scratch":
                user_prompt_template = user_prompts["scratch"][modalities]
                user_prompt = user_prompt_template.format(
                    description=task["description"],
                    code=task["base_shape_code"],
                    query=task["query"],
                    variables=task["variables"],
                )
            elif task_type == "tweak":
                user_prompt_template = user_prompts["tweak"][task_mode][modalities]
                user_prompt = user_prompt_template.format(
                    description=task["description"],
                    code=task["base_shape_code"],
                    query=task["query"],
                    variables=task["variables"],
                )

            user_prompt += "\n" + user_prompt_final_piece.format(
                variables=task["variables"]
            )

            # Handle watermarking for code_edit mode
            base_image = task["base_shape"]
            result_image = task["result_shape"]
            if task_mode == "code_edit" and modalities == "image+image":
                watermarked_path = temp_manager.create_subfolder("watermarked")
                base_image = watermark_and_save(
                    task["base_shape"], watermarked_path, "1"
                )
                result_image = watermark_and_save(
                    task["result_shape"], watermarked_path, "2"
                )

            # Use DSPy for code generation
            with dspy.context(lm=self.lm):
                if prompting_mode == "few-shot":
                    return self._process_few_shot(task, system_prompt)
                else:
                    if task_type == "scratch":
                        prediction = self.predictor(
                            system_prompt=system_prompt,
                            task_description=task["description"],
                            base_code=task.get("base_shape_code", ""),
                            query=task.get("query", ""),
                            variables=task.get("variables", ""),
                        )
                        return prediction.turtle_code
                    elif task_type == "tweak":
                        # For tweak tasks, combine system prompt with original code and modification
                        full_prompt = f"{system_prompt}\n\nOriginal code:\n{task['base_shape_code']}\n\nModification request:\n{task['query']}"
                        prediction = self.predictor(
                            system_prompt=system_prompt,
                            task_description=full_prompt,
                            base_code=task.get("base_shape_code", ""),
                            query=task.get("query", ""),
                            variables=task.get("variables", ""),
                        )
                        return prediction.turtle_code

        except Exception as e:
            print(f"Error processing task: {e}")
            return None

    def _process_few_shot(self, task, system_prompt):
        """Process a task using few-shot learning."""

        # For few-shot, we need examples - simplified version here
        examples_text = "Generate turtle code based on the description."

        with dspy.context(lm=self.lm):
            prediction = self.predictor(
                system_prompt=system_prompt,
                task_description=f"Examples: {examples_text}\n\nTarget: {task['description']}",
                base_code="",
                query="",
                variables=task.get("variables", ""),
            )
            return prediction.turtle_code


def eval_dspy(
    model_name="gpt4-v",
    task_type="scratch",
    task_mode="code_generation",
    modalities="image_only",
    prompting_mode="cot",
    code_framework="turtle",
    save_responses=False,
):
    """Main evaluation function using DSPy framework."""

    # Load dataset
    tasks_config_path = "dataset.jsonl"
    config = []
    with open(tasks_config_path, "r") as file:
        for line in file:
            json_object = json.loads(line)
            config.append(json_object)

    # Filter tasks based on task_type and modalities
    if task_type == "scratch" and "text" in modalities:
        subset = [
            conf
            for conf in config
            if conf["question_number"] == 1 and conf["description"] != None
        ]
    elif task_type == "scratch" and "text" not in modalities:
        subset = [conf for conf in config if conf["question_number"] == 1]
    elif task_type == "tweak":
        subset = [conf for conf in config if conf["question_number"] != 1]
    else:
        subset = []

    # Initialize DSPy agent
    agent = TurtleBenchDSPyAgent(model_name)

    # Setup output directories
    time = datetime.datetime.now().strftime("%d-%m_%H%M")
    run_name = "-".join(
        [model_name, task_type, task_mode, modalities, prompting_mode, time]
    )

    if save_responses:
        responses_path = ".responses/" + run_name
        os.makedirs(responses_path, exist_ok=True)
        images_path = responses_path + "_images/"
        os.makedirs(images_path, exist_ok=True)
    else:
        global temp_manager
        temp_manager = TempDirManager()
        responses_path = temp_manager.create_subfolder(run_name)
        images_path = temp_manager.create_subfolder(run_name + "_images")

    # Evaluation loop
    solved_counter = 0
    pbar = tqdm(total=len(subset), desc="Processing tasks with DSPy")

    run_settings = {
        "model_name": model_name,
        "task_type": task_type,
        "task_mode": task_mode,
        "modalities": modalities,
        "prompting_mode": prompting_mode,
        "time": time,
    }
    update_report(run_setting=run_settings.copy(), accuracy=None, solved_counter=None)

    for task in subset:
        task_name = str(task["id"]) + "_" + str(task["question_number"])

        # Use DSPy agent to generate code
        response = agent(
            task=task,
            task_type=task_type,
            task_mode=task_mode,
            modalities=modalities,
            prompting_mode=prompting_mode,
        )

        # Ensure we have a response
        if response is None:
            print(f"DSPy failed for task {task_name}, using empty response")
            response = ""

        response_piece_of_code = preprocess_response(response)

        with open(os.path.join(responses_path, task_name + ".txt"), "w") as f:
            f.write(response)

        # Execute and evaluate code
        code_runnable = code_to_image(
            response_piece_of_code, task_name, save_path=images_path
        )
        if code_runnable:
            solved = calculate_accuracy(
                task_name, source_path="autotest/source", response_path=images_path
            )
            if solved:
                solved_counter += 1

        current_accuracy = (solved_counter / (pbar.n + 1)) * 100
        pbar.set_postfix(accuracy=f"{current_accuracy:.2f}%")
        pbar.update(1)

    pbar.close()
    if not save_responses:
        temp_manager.close_temp_directory()

    final_accuracy = (solved_counter * 100 / len(subset)) if len(subset) > 0 else 0
    update_report(run_settings, solved_counter, final_accuracy)
    print(
        f"DSPy Accuracy: {final_accuracy:.2f}%, Solved {solved_counter} from {len(subset)}"
    )


if __name__ == "__main__":
    LOCAL_MODEL_ID = "zai-org/glm-4.6v-flash"
    parser = argparse.ArgumentParser(
        description="Run evaluation on different models and tasks using DSPy framework."
    )

    parser.add_argument(
        "--model_name",
        type=str,
        default=f"lm_studio/{LOCAL_MODEL_ID}",
        help=f'The model name to use. Default is a local model, "lm_studio/{LOCAL_MODEL_ID}".',
    )
    parser.add_argument(
        "--task_type",
        type=str,
        default="scratch",
        help='Type of task to perform. Options are "scratch" or "tweak". Default is "scratch".',
    )
    parser.add_argument(
        "--task_mode",
        type=str,
        default="code_generation",
        help='Mode of the task. Options are "code_generation" and "code_edit". Default is "code_generation".',
    )
    parser.add_argument(
        "--modalities",
        type=str,
        default="text_only",
        help='Modalities to use. Options are "image_only", "text_only", "image+text", and "image+image". Default is "text_only".',
    )
    parser.add_argument(
        "--prompting_mode",
        type=str,
        default="cot",
        help='Prompting mode to use. Options are "cot", "basic", and "few-shot". Default is "cot".',
    )
    parser.add_argument(
        "--code_framework",
        type=str,
        default="turtle",
        help='Framework for code generation. Default is "turtle".',
    )
    parser.add_argument(
        "--save_responses",
        action="store_true",
        help="Save responses to files. Does not save by default.",
    )

    args = parser.parse_args()

    eval_dspy(
        model_name=args.model_name,
        task_type=args.task_type,
        task_mode=args.task_mode,
        modalities=args.modalities,
        prompting_mode=args.prompting_mode,
        code_framework=args.code_framework,
        save_responses=args.save_responses,
    )
