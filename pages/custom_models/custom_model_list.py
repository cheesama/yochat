import mesop as me

from components.global_header import global_header_component


@me.page(path="/custom_model")
def custom_model_list_page():
    # 글로벌 헤더 추가
    global_header_component()

    me.text("custom_model_list")
