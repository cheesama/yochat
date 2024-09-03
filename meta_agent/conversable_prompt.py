from langchain_core.prompts import PromptTemplate

# 기본 시스템 프롬프트
system_prompt = """You are an expert assistant capable of engaging in a conversation to break down complex tasks and execute them step by step."""

# 기본 Conversable Agent를 위한 프롬프트 템플릿
base_prompt = """# Conversation:
You will be provided with a task description. Engage in a step-by-step conversation, ask clarifying questions if needed, break down the task into manageable sub-tasks, and execute them. Provide detailed reasoning for each step you take.

# Task Description:
{task_description}

# Conversation and Solution:
"""


def get_task_complexity_prompt():
    template = """
    주어진 작업의 복잡도를 평가하고 1에서 10까지의 척도로 점수를 매겨주세요.
    1은 매우 간단한 작업을, 10은 매우 복잡한 작업을 나타냅니다.
    작업 설명: {task_description}
    복잡도 점수 (1-10):
    """
    return PromptTemplate(template=template, input_variables=["task_description"])


def get_conversable_prompt():
    template = """
    다음 작업을 수행하세요:
    {task_description}
    """
    return PromptTemplate(template=template, input_variables=["task_description"])


def get_subtask_prompt():
    template = """
    다음 작업을 더 작은 서브태스크로 분해하세요:
    {task_description}
    
    각 서브태스크를 새 줄에 나열하세요.
    """
    return PromptTemplate(template=template, input_variables=["task_description"])


def get_execution_plan_prompt():
    template = """
    다음은 복잡한 작업을 수행하기 위해 실행된 서브태스크들의 결과입니다:
    {sub_tasks}
    
    이 결과들을 종합하여 최종 해결책을 제시하세요.
    """
    return PromptTemplate(template=template, input_variables=["sub_tasks"])


# 서브태스크 분해를 위한 프롬프트 템플릿
subtask_prompt = """# Sub-Task:
Analyze the provided task and decompose it into clear, manageable sub-tasks. Indicate whether the sub-tasks should be performed sequentially or in parallel. Each sub-task should be a distinct and logical step towards solving the overall task.

# Task Description:
{task_description}

# Sub-Tasks:
"""


def get_subtask_prompt(task_description):
    """
    서브태스크 분해를 위한 프롬프트 템플릿 생성
    :param task_description: 작업 설명
    :return: 서브태스크 분해 프롬프트 템플릿
    """
    prompt_template = PromptTemplate(
        input_variables=["task_description"], template=subtask_prompt
    )
    return system_prompt, prompt_template


# 서브태스크 수행 방식 및 결과 종합 방식을 결정하는 프롬프트 템플릿
execution_plan_prompt = """# Execution Plan:
Given the sub-tasks listed below, analyze the relationship and dependencies among them. Determine whether the sub-tasks should be performed sequentially or in parallel. Finally, decide how to combine the results of these sub-tasks into a comprehensive final answer.

# Sub-Tasks:
{sub_tasks}

# Execution Plan and Final Answer Strategy:
"""


def get_execution_plan_prompt(sub_tasks):
    """
    서브태스크 수행 방식 및 결과 종합 방식을 결정하는 프롬프트 템플릿 생성
    :param sub_tasks: 서브태스크 리스트
    :return: 수행 방식 및 결과 종합 프롬프트 템플릿
    """
    prompt_template = PromptTemplate(
        input_variables=["sub_tasks"], template=execution_plan_prompt
    )
    return system_prompt, prompt_template.template


# 서브태스크 결과 종합을 위한 프롬프트 템플릿
combine_results_prompt = """# Combine Sub-Task Results:
The following sub-tasks have been completed. Based on the nature of the task, combine the results into a comprehensive final answer. Ensure that the combination reflects the logical flow of the sub-tasks, whether they were performed sequentially or in parallel.

# Sub-Task Results:
{sub_task_results}

# Final Answer:
"""


def get_combine_results_prompt(sub_task_results):
    """
    서브태스크 결과를 종합하기 위한 프롬프트 템플릿 생성
    :param sub_task_results: 서브태스크 결과 리스트
    :return: 서브태스크 결과 종합 프롬프트 템플릿
    """
    prompt_template = PromptTemplate(
        input_variables=["sub_task_results"], template=combine_results_prompt
    )
    return system_prompt, prompt_template.template


def get_task_evaluation_prompt(task_description, available_tools):
    """
    작업의 특성을 평가하고 실행 가능성을 판단하기 위한 프롬프트 템플릿 생성
    """
    system_prompt = (
        "당신은 작업의 특성을 평가하고 실행 전략을 결정하는 전문가 AI 어시스턴트입니다."
    )

    prompt_template = """
    작업 설명: {task_description}
    
    사용 가능한 도구 목록:
    {available_tools}
    
    위의 작업에 대해 다음 기준으로 평가해주세요:
    1. 작업의 복잡성
    2. 주어진 도구의 적절성 및 충분성
    3. 서브태스크로 분해할 필요성
    
    평가 후, 다음 중 하나로 응답해주세요:
    - "DIRECT": 작업이 간단하거나, 복잡하더라도 주어진 도구만으로 직접 수행 가능한 경우
    - "SUBTASKS": 작업이 복잡하고 주어진 도구를 활용하여 서브태스크로 분해해야 하는 경우
    - "INSUFFICIENT": 작업 수행에 필요한 도구가 부족하여 적절한 답변이 어려운 경우
    
    응답 (DIRECT, SUBTASKS, 또는 INSUFFICIENT):
    """

    return system_prompt, prompt_template
