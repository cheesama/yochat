import re
import logging
import dotenv

dotenv.load_dotenv()

from pydantic import Field
from llama_index.core.agent import FunctionCallingAgentWorker, ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.llms.cohere import Cohere
from llama_agents import (
    AgentService,
    AgentOrchestrator,
    ControlPlaneServer,
    SimpleMessageQueue,
    ServerLauncher,
    CallableMessageConsumer,
)

from meta_agent.conversable_prompt import (
    get_task_complexity_prompt,
    get_conversable_prompt,
    get_subtask_prompt,
    get_execution_plan_prompt,
)


# 로거 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_llm(llm_type="cohere"):
    # if llm_type == "openai":
    #     return OpenAI()
    # elif llm_type == "bedrock":
    #     return Bedrock()
    return Cohere(model_name="command-r")


class ConversableAgent:
    def __init__(self, llm_type="cohere", tools=None):
        self.llm = get_llm(llm_type)

        # create our multi-agent framework components
        message_queue = SimpleMessageQueue()
        control_plane = ControlPlaneServer(
            message_queue=message_queue,
            orchestrator=AgentOrchestrator(llm=self.llm),
        )

        self.system_prompt = "You are an expert assistant capable of engaging in a conversation to solve complex tasks."
        logger.info(
            f"ConversableAgent 초기화 완료 (LLM 타입: {llm_type}, 모델: {self.llm.model_name})"
        )

    def add_tool(self, fn):
        tool = FunctionTool.from_defaults(fn=fn)
        self.tools.append(tool)

    def remove_tool(self, tool_name: str):
        self.tools = [tool for tool in self.tools if tool.name != tool_name]

    def evaluate_task_complexity(self, task_description: str) -> int:
        prompt = get_task_complexity_prompt()
        chain = prompt | self.llm

        logger.info(f"작업 복잡성 평가 시작: {task_description}")
        response = chain.invoke({"task_description": task_description})
        logger.info(f"LLM 응답: {response}")

        # 응답에서 숫자 추출
        complexity_match = re.search(r"\b([1-9]|10)\b", response)
        if complexity_match:
            complexity = int(complexity_match.group(1))
        else:
            logger.warning("복잡도를 추출할 수 없습니다. 기본값 5를 사용합니다.")
            complexity = 5

        logger.info(f"작업 복잡성 평가 결과: {complexity}")
        return complexity

    def execute_task(self, task_description: str) -> str:
        complexity = self.evaluate_task_complexity(task_description)

        if complexity > 5:
            logger.info("복잡한 작업으로 판단. 서브태스크로 분해 실행")
            return self._execute_with_subtasks(task_description)
        else:
            logger.info("단순한 작업으로 판단. 단일 태스크로 실행")
            return self._execute_single_task(task_description)

    def _execute_with_subtasks(self, task_description: str) -> str:
        sub_tasks = self.decompose_task(task_description)
        logger.info(f"서브태스크 목록: {sub_tasks}")

        logger.info("서브태스크 순차 실행 시작")
        final_solution = self.execute_subtasks(sub_tasks)
        return final_solution

    def _execute_single_task(self, task_description: str) -> str:
        prompt = get_conversable_prompt()
        chain = prompt | self.llm

        logger.info(f"단일 태스크 실행 시작: {task_description}")
        result = chain.invoke({"task_description": task_description})
        logger.info(f"단일 태스크 실행 결과: {result}")

        return result

    def decompose_task(self, task_description: str) -> list:
        prompt = get_subtask_prompt()
        chain = prompt | self.llm

        sub_tasks = chain.invoke({"task_description": task_description})
        logger.info(f"Sub-tasks: {sub_tasks}")

        return sub_tasks.split("\n")

    def execute_subtasks(self, sub_tasks: list) -> str:
        results = []

        for i, sub_task in enumerate(sub_tasks):
            logger.info(f"서브태스크 {i+1} 실행 시작: {sub_task}")
            result = self._execute_single_task(sub_task)
            logger.info(f"서브태스크 {i+1} 실행 결과: {result}")
            results.append(result)

        combine_prompt = get_execution_plan_prompt()
        chain = combine_prompt | self.llm

        logger.info("최종 결과 도출 시작")
        final_result = chain.invoke({"sub_tasks": "\n".join(results)})
        logger.info(f"최종 결과: {final_result}")

        return final_result


def task_decomposition(task_description: str = Field(description="태스크 설명")) -> str:
    """태스크를 서브태스크들로 분해"""

    return Tool(
        name="TaskDecompositionAndExecution",
        func=lambda task_description: agent.execute_task(task_description),
        description="Decompose tasks into sub-tasks and execute them",
    )


# 시스템에서 초기 로딩 시 에이전트 설정 및 기본 툴 추가
def initialize_conversable_agent_system(llm_type="cohere"):
    agent = ConversableAgent(llm_type=llm_type)

    # add default tools
    agent.add_tool(task_decomposition)

    return agent


# 시스템에서 에이전트 실행 예시
def main():
    agent_system = initialize_conversable_agent_system()

    task_description = "영수가 5개 중에 3개의 사과를 먹었어, 영희한테 모든 사과를 준다고 할 때 몇개를 받아?"

    final_solution = agent_system.execute_task(task_description)
    print("Final Solution:", final_solution)


if __name__ == "__main__":
    main()
