import random
import time

import mesop as me
import mesop.labs as mel

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
    for line in random.sample(LINES, random.randint(3, len(LINES) - 1)):
        time.sleep(0.3)
        yield line + " "


LINES = [
    "Mesop is a Python-based UI framework designed to simplify web UI development for engineers without frontend experience.",
    "It leverages the power of the Angular web framework and Angular Material components, allowing rapid construction of web demos and internal tools.",
    "With Mesop, developers can enjoy a fast build-edit-refresh loop thanks to its hot reload feature, making UI tweaks and component integration seamless.",
    "Deployment is straightforward, utilizing standard HTTP technologies.",
    "Mesop's component library aims for comprehensive Angular Material component coverage, enhancing UI flexibility and composability.",
    "It supports custom components for specific use cases, ensuring developers can extend its capabilities to fit their unique requirements.",
    "Mesop's roadmap includes expanding its component library and simplifying the onboarding processs.",
]
