import dspy
from typing import List, Optional


class TurtleCodeGeneration(dspy.Signature):
    """Generate Python turtle code to create geometric patterns based on visual input and descriptions."""
    
    system_instruction: str = dspy.InputField(desc="System instructions for turtle code generation")
    task_description: str = dspy.InputField(desc="Description of the geometric pattern to create")
    base_shape_code: Optional[str] = dspy.InputField(desc="Existing turtle code to modify (for tweak tasks)")
    query: Optional[str] = dspy.InputField(desc="Specific modification instructions (for tweak tasks)")
    variables: Optional[str] = dspy.InputField(desc="Variable definitions for the task")
    base_image: Optional[str] = dspy.InputField(desc="Base shape image path")
    result_image: Optional[str] = dspy.InputField(desc="Target result image path")
    
    turtle_code: str = dspy.OutputField(desc="Complete Python turtle code to generate the pattern")
    explanation: Optional[str] = dspy.OutputField(desc="Explanation of the generated code logic")


class TurtleCodeEditing(dspy.Signature):
    """Edit existing turtle code to achieve specific modifications."""
    
    system_instruction: str = dspy.InputField(desc="System instructions for turtle code editing")
    original_code: str = dspy.InputField(desc="Original turtle code to be modified")
    modification_query: str = dspy.InputField(desc="Description of required modifications")
    variables: Optional[str] = dspy.InputField(desc="Variable definitions for the task")
    base_image: Optional[str] = dspy.InputField(desc="Current state image path")
    target_image: Optional[str] = dspy.InputField(desc="Target result image path")
    
    modified_code: str = dspy.OutputField(desc="Modified turtle code")
    changes_summary: Optional[str] = dspy.OutputField(desc="Summary of changes made to the code")


class TurtleFewShotLearning(dspy.Signature):
    """Generate turtle code by learning from few-shot examples."""
    
    system_instruction: str = dspy.InputField(desc="System instructions for few-shot learning")
    examples: List[str] = dspy.InputField(desc="Few-shot examples with code and images")
    target_description: str = dspy.InputField(desc="Description of target pattern")
    target_image: Optional[str] = dspy.InputField(desc="Target result image path")
    variables: Optional[str] = dspy.InputField(desc="Variable definitions for the task")
    
    turtle_code: str = dspy.OutputField(desc="Generated turtle code following the pattern")
    reasoning: Optional[str] = dspy.OutputField(desc="Reasoning about how examples guided the generation")


class TurtleCodeOptimization(dspy.Signature):
    """Optimize turtle code for better performance, readability, or accuracy."""
    
    original_code: str = dspy.InputField(desc="Original turtle code")
    optimization_goal: str = dspy.InputField(desc="What to optimize (performance, readability, accuracy)")
    constraints: Optional[str] = dspy.InputField(desc="Any constraints or requirements")
    
    optimized_code: str = dspy.OutputField(desc="Optimized turtle code")
    improvements: Optional[str] = dspy.OutputField(desc="Description of improvements made")


class TurtleErrorCorrection(dspy.Signature):
    """Debug and fix errors in turtle code."""
    
    erroneous_code: str = dspy.InputField(desc="Turtle code with errors")
    error_description: Optional[str] = dspy.InputField(desc="Description of encountered errors")
    expected_output: Optional[str] = dspy.InputField(desc="Description of expected output")
    
    corrected_code: str = dspy.OutputField(desc="Fixed turtle code")
    error_analysis: Optional[str] = dspy.OutputField(desc="Analysis of what was wrong and how it was fixed")


class TurtleSimilarityAssessment(dspy.Signature):
    """Assess similarity between generated pattern and target pattern."""
    
    generated_code: str = dspy.InputField(desc="Code that was executed")
    generated_image_path: str = dspy.InputField(desc="Path to generated result image")
    target_image_path: str = dspy.InputField(desc="Path to target reference image")
    
    similarity_score: float = dspy.OutputField(desc="Similarity score between 0.0 and 1.0")
    differences_description: str = dspy.OutputField(desc="Description of key differences between patterns")
    is_match: bool = dspy.OutputField(desc="Whether patterns match sufficiently")