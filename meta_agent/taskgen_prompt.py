from langchain import PromptTemplate

# 기본 시스템 프롬프트
system_prompt = """You are an expert assistant specialized in breaking down complex tasks into manageable sub-tasks and executing them efficiently. Please analyze the problem, decompose it into sub-tasks, and solve them step by step."""

# 작업 분해 및 실행을 위한 프롬프트 템플릿
base_prompt = """# Task:
{task_description}

# Your Goal:
1. Analyze the task and break it down into clear, manageable sub-tasks.
2. Execute each sub-task step by step.
3. Provide the final solution based on the sub-tasks you performed.

# Sub-Tasks and Solution:
"""


# 프롬프트 템플릿 정의
def get_taskgen_prompt(task_description):
    prompt_template = PromptTemplate(
        input_variables=["task_description"], template=base_prompt
    )
    return system_prompt, prompt_template
