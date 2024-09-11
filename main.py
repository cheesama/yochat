import random
import time

import mesop as me
import mesop.labs as mel

from meta_agent.agent.main_agent import MainAgent

from pages.apis.api_list import api_list_page
from pages.custom_models.custom_model_list import custom_model_list_page
from pages.custom_tools.custom_tool_list import custom_tool_list_page
from pages.document_store.document_store_list import document_store_list_page
from pages.prompts.prompt_list import prompt_list_page

from components.global_header import global_header_component

SIDENAV_WIDTH = 300


@me.stateclass
class State:
    sidenav_open: bool


def on_click(e: me.ClickEvent):
    s = me.state(State)
    s.sidenav_open = not s.sidenav_open


@me.page(
    path="/chat",
    title="YoChat",
)
def chat_page():
    state = me.state(State)

    # 글로벌 헤더 추가
    global_header_component()

    mel.chat(transform, title="", bot_user="YoChat")


def transform(input: str, history: list[mel.ChatMessage]):
    state = me.state(State)
    agent = MainAgent(timeout=60, verbose=True)

    # 에이전트에 쿼리 전송 및 응답 생성
    response = agent.run(query=input)

    # 응답 반환
    yield response
