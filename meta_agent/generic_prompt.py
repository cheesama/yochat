from langchain import PromptTemplate

# 기본 시스템 프롬프트
system_prompt = """You are an expert assistant specialized in providing accurate answers to a wide range of questions. Carefully analyze the question and provide a detailed, well-reasoned response."""

# 일반적인 질문에 대한 프롬프트 템플릿
base_prompt = """# Question:
{question}

# Task:
Provide a clear, concise, and accurate answer to the above question. Where necessary, include explanations or reasoning that supports your answer.

# Answer:
"""


# 프롬프트 템플릿 정의
def get_generic_prompt(question):
    prompt_template = PromptTemplate(input_variables=["question"], template=base_prompt)
    return system_prompt, prompt_template
