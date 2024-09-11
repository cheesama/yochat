import logging
import os
from typing import Any, List
from dotenv import load_dotenv
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.tools import ToolSelection, ToolOutput, FunctionTool
from llama_index.core.tools.types import BaseTool
from llama_index.llms.cohere import Cohere

from default_tools import web_search_tool, python_repl_tool

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Set the logging format
    handlers=[
        # logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ],
)


class InputEvent(Event):
    input: list[ChatMessage]


class InitializeEvent(Event):
    tools: List[FunctionTool] = []
    vector_db: List[str] = []
    task: str


class TaskDecompositionEvent(Event):
    subtasks: List[str]


class ToolCallEvent(Event):
    tool_calls: list[ToolSelection]


class FunctionOutputEvent(Event):
    output: ToolOutput


class DefaultFlow(Workflow):
    def __init__(
        self,
        *args: Any,
        llm: FunctionCallingLLM | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.llm = llm or Cohere(api_key=os.getenv("CO_API_KEY"), temperature=0.1)
        assert self.llm.metadata.is_function_calling_model

        self.chat_memory = ChatMemoryBuffer.from_defaults(llm=llm)
        self.sources = []
        # register default tools
        self.default_tools = [
            FunctionTool.from_defaults(web_search_tool),
            FunctionTool.from_defaults(python_repl_tool),
        ]

    @step
    async def prepare_chat_history(self, event: StartEvent) -> InputEvent:
        # clear sources
        self.sources = []

        # get user input
        user_input = event.input
        user_msg = ChatMessage(role="user", content=user_input)
        self.chat_memory.put(user_msg)

        # get chat history
        chat_history = self.chat_memory.get()
        return InputEvent(input=chat_history)

    @step
    async def register_exist_tools_and_vector_db(
        self, event: InputEvent
    ) -> InitializeEvent:
        # TODO: register exist tools and vector db
        return InitializeEvent(tools=self.default_tools, task=event.input[-1].content)

    @step
    async def decompsite_task(self, event: InitializeEvent) -> TaskDecompositionEvent:
        task = event.task

        prompt = f"""
        You are a helpful assistant. You are given a task and a list of tools that can be used to complete the task.
        You need to decomposite this task into subtasks. If it seems too simple, you don't need to decompose it.
        When you decompose the task, you need to make sure that each subtask is a standalone task that can be completed by an agent.
        When you are done, you need to return the subtasks in a list.
        If proper tools are provided, you need to use them to complete the task. then return the subtasks with tool calls.
        just return subtasks, withtout any other explanation with list format like ['subtask1', 'subtask2', 'subtask3'].

        task: 

        """

        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=prompt),
        ]
        messages.extend(self.chat_memory.get())

        response = await self.llm.achat(messages)

        logging.info(f"Decomposed subtasks: {response.message.content}")
        # response = eval(response.message.content.split("assistant:")[-1])
        response = response.message.content.split(".")
        return TaskDecompositionEvent(subtasks=response)

    @step
    async def execute_subtasks(self, event: TaskDecompositionEvent) -> StopEvent:
        subtasks = event.subtasks
        for subtask in subtasks:
            response = await self.llm.achat_with_tools(
                tools=self.default_tools,
                user_msg=subtask,
                verbose=True,
                allow_parallel_tool_calls=True,
            )
            logging.info(f"Executing subtask: {subtask}, response: {response}")

            tool_calls = self.llm.get_tool_calls_from_response(
                response, error_on_no_tool_call=False
            )
            if tool_calls:
                logging.info(f"Tool calls: {tool_calls}")
                return ToolCallEvent(tool_calls=tool_calls)
            else:
                logging.info(f"No tool calls found in response: {response}")

        return StopEvent()

    @step
    async def handle_tool_calls(self, ev: ToolCallEvent) -> TaskDecompositionEvent:
        tool_calls = ev.tool_calls
        tools_by_name = {tool.metadata.get_name(): tool for tool in self.tools}


async def main():
    w = DefaultFlow(timeout=60, verbose=True)
    result = await w.run(input="내일 서울 날씨 뭐야?")
    print(str(result))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
