import mesop as me
import time
from typing import Callable, Literal


@me.stateclass
class State:
    step: int = 1
    radio_value: str = "자동"
    index_mode: str = "자동"
    is_segmented: bool = False  # 추가 설정을 위한 상태 변수
    snackbar_visible: bool = False
    snackbar_message: str = ""
    snackbar_duration: int = 3
    is_sidebar_visible: bool = True  # 사이드바 가시성 상태
    progress: int = 0  # 임베딩 진행률 상태
    embedding_completed: bool = False  # 임베딩 완료 상태


def show_snackbar(message: str):
    state = me.state(State)
    state.snackbar_message = message
    state.snackbar_visible = True
    yield
    time.sleep(state.snackbar_duration)
    state.snackbar_visible = False
    yield


def toggle_sidebar():
    state = me.state(State)
    state.is_sidebar_visible = not state.is_sidebar_visible


def start_embedding():
    state = me.state(State)
    state.progress = 0
    state.embedding_completed = False
    for i in range(101):
        state.progress = i
        time.sleep(0.05)  # 임베딩 진행을 시뮬레이션하는 딜레이
        yield
    state.embedding_completed = True
    yield


@me.page(
    path="/document_store_create",
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io", "https://huggingface.co"]
    ),
)
def document_store_create_page():
    state = me.state(State)

    # 스낵바 컴포넌트
    snackbar(
        label=state.snackbar_message,
        is_visible=state.snackbar_visible,
        horizontal_position="center",
        vertical_position="end",
    )

    with me.box(
        style=me.Style(
            display="grid",
            grid_template_columns="1fr 3fr",
            gap=20,
            padding=me.Padding.all(16),
        )
    ):

        # 좌측 네비게이션 패널
        with me.box(
            style=me.Style(
                background="white",
                padding=me.Padding.all(16),
                border=me.Border.all(
                    me.BorderSide(width=2, color="#e0e0e0", style="solid")
                ),
                border_radius=8,
            )
        ):
            me.text("지식 생성", style=me.Style(font_size=20, font_weight="bold"))
            me.text(
                "1. 데이터 소스 선택",
                style=me.Style(
                    color="#3b82f6" if state.step == 1 else "gray",
                    font_weight="bold",
                    margin=me.Margin(top=10),
                ),
            )
            me.text(
                "2. 텍스트 전처리 및 클리닝",
                style=me.Style(
                    color="#3b82f6" if state.step == 2 else "gray",
                    margin=me.Margin(top=10),
                ),
            )
            me.text(
                "3. 실행 및 완료",
                style=me.Style(
                    color="#3b82f6" if state.step == 3 else "gray",
                    margin=me.Margin(top=10),
                ),
            )

        # 메인 컨텐츠 영역
        with me.box(
            style=me.Style(
                background="white",
                padding=me.Padding.all(16),
                border=me.Border.all(
                    me.BorderSide(width=2, color="#e0e0e0", style="solid")
                ),
                border_radius=8,
                position="relative",
            )
        ):
            if state.step == 1:
                # 데이터 소스 선택 섹션
                me.text(
                    "데이터 소스 선택",
                    style=me.Style(
                        font_size=24, font_weight="bold", margin=me.Margin(bottom=16)
                    ),
                )

                with me.box(
                    style=me.Style(display="flex", gap=20, margin=me.Margin(bottom=16))
                ):
                    me.button(
                        "텍스트 파일에서 가져오기",
                        on_click=lambda _: show_snackbar("텍스트 파일 선택됨"),
                    )
                    me.button(
                        "BigQuery에서 가져오기",
                        on_click=lambda _: show_snackbar("BigQuery 선택됨"),
                    )

                me.text(
                    "텍스트 파일 업로드",
                    style=me.Style(
                        font_size=16, font_weight="bold", margin=me.Margin(bottom=8)
                    ),
                )

                with me.box(
                    style=me.Style(
                        border=me.Border.all(
                            me.BorderSide(width=2, color="#e0e0e0", style="dashed")
                        ),
                        padding=me.Padding.all(16),
                        margin=me.Margin(bottom=16),
                    )
                ):
                    me.text("파일을 끌어다 놓거나 ", style=me.Style(display="inline"))
                    me.text(
                        "TXT, MARKDOWN, PDF, HTML, XLSX, XLS, DOCX, CSV을(를) 지원합니다. 파일당 최대 크기는 15MB입니다.",
                        style=me.Style(
                            font_size=12, color="gray", margin=me.Margin(top=8)
                        ),
                    )

                me.button(
                    "다음",
                    on_click=lambda _: go_to_step(2),
                    style=me.Style(
                        background="#3b82f6",
                        color="white",
                        padding=me.Padding.symmetric(horizontal=16, vertical=8),
                    ),
                )

            elif state.step == 2:
                # 텍스트 전처리 및 클리닝 섹션
                me.text(
                    "텍스트 전처리 및 클리닝",
                    style=me.Style(
                        font_size=24, font_weight="bold", margin=me.Margin(bottom=16)
                    ),
                )

                # 청크 설정
                me.text(
                    "청크 설정",
                    style=me.Style(font_size=16, margin=me.Margin(bottom=8)),
                )
                me.radio(
                    on_change=lambda _: show_snackbar("자동 설정만 가능합니다."),
                    options=[
                        me.RadioOption(label="자동", value="자동"),
                        me.RadioOption(label="사용자 설정", value="사용자 설정"),
                    ],
                    value=state.radio_value,
                )
                me.text(
                    "자동 설정만 가능합니다. (추후 개발 예정)",
                    style=me.Style(font_size=12, color="gray", margin=me.Margin(top=8)),
                )

                # 인덱스 모드
                me.text(
                    "인덱스 모드",
                    style=me.Style(font_size=16, margin=me.Margin(top=16)),
                )
                me.radio(
                    on_change=lambda _: show_snackbar("자동 설정만 가능합니다."),
                    options=[
                        me.RadioOption(label="자동", value="자동"),
                        me.RadioOption(label="사용자 설정", value="사용자 설정"),
                    ],
                    value=state.index_mode,
                )
                me.text(
                    "자동 설정만 가능합니다. (추후 개발 예정)",
                    style=me.Style(font_size=12, color="gray", margin=me.Margin(top=8)),
                )

                # 추가 설정: 질문과 답변 형식으로 세그먼트화
                me.checkbox(
                    "질문과 답변 형식으로 세그먼트화",
                    on_change=lambda _: show_snackbar("추후 개발 예정"),
                    checked=False,
                )
                me.text(
                    "추후 개발 예정",
                    style=me.Style(font_size=12, color="gray", margin=me.Margin(top=8)),
                )

                # 실행 버튼을 우하단에 위치시킴
                with me.box(
                    style=me.Style(position="absolute", right="320px", bottom="16px")
                ):
                    me.button(
                        "실행",
                        on_click=lambda _: go_to_step(3),
                        style=me.Style(
                            background="#3b82f6",
                            color="white",
                            padding=me.Padding.symmetric(horizontal=16, vertical=8),
                        ),
                    )

                # 우측 미리보기 패널 (토글 가능)
                if state.is_sidebar_visible:
                    with me.box(
                        style=me.Style(
                            position="absolute",
                            right="0px",
                            width="300px",
                            top="0px",
                            bottom="0px",
                            border=me.Border(
                                left=me.BorderSide(
                                    width=2, color="#e0e0e0", style="solid"
                                )
                            ),
                        )
                    ):
                        me.text(
                            "미리보기",
                            style=me.Style(
                                font_size=18,
                                font_weight="bold",
                                margin=me.Margin(bottom=16),
                            ),
                        )

                        # 예제 미리보기 항목
                        for i in range(1, 6):
                            me.text(
                                f"#00{i} 미리보기 항목",
                                style=me.Style(
                                    font_size=14, margin=me.Margin(bottom=8)
                                ),
                            )

                # 사이드바 토글 버튼
                me.button(
                    "미리 보기",
                    on_click=lambda _: toggle_sidebar(),
                    style=me.Style(position="absolute", top="16px", right="16px"),
                )

            elif state.step == 3:
                # 실행 및 완료 섹션
                me.text(
                    "🎉 Document Store 가 생성되었습니다",
                    style=me.Style(
                        font_size=24, font_weight="bold", margin=me.Margin(bottom=16)
                    ),
                )
                me.text(
                    "Document Store 이름 : ",
                    style=me.Style(
                        font_size=18, font_weight="bold", margin=me.Margin(bottom=8)
                    ),
                )
                me.text(
                    "임베딩이 완료되었습니다",
                    style=me.Style(color="gray", margin=me.Margin(bottom=8)),
                )

                if not state.embedding_completed:
                    me.progress_spinner()
                    # me.run_task(start_embedding())
                else:
                    me.text(
                        "임베딩이 완료되었습니다",
                        style=me.Style(
                            font_size=16,
                            font_weight="bold",
                            color="green",
                            margin=me.Margin(bottom=16),
                        ),
                    )

                me.text(
                    "세그먼트 규칙",
                    style=me.Style(
                        font_size=16, font_weight="bold", margin=me.Margin(bottom=8)
                    ),
                )
                me.text("자동", style=me.Style(margin=me.Margin(bottom=8)))
                me.text(
                    "청크의 길이",
                    style=me.Style(
                        font_size=16, font_weight="bold", margin=me.Margin(bottom=8)
                    ),
                )
                me.text("500", style=me.Style(margin=me.Margin(bottom=8)))
                me.text(
                    "텍스트 전처리",
                    style=me.Style(
                        font_size=16, font_weight="bold", margin=me.Margin(bottom=8)
                    ),
                )
                me.text("자동", style=me.Style(margin=me.Margin(bottom=8)))

                with me.box(
                    style=me.Style(
                        margin=me.Margin(top=16),
                        padding=me.Padding.all(16),
                        background="#f1f5f9",
                        border_radius=8,
                    )
                ):
                    me.text(
                        "다음 단계는 무엇인가요",
                        style=me.Style(
                            font_size=18, font_weight="bold", margin=me.Margin(bottom=8)
                        ),
                    )
                    me.text(
                        "문서 인덱싱이 완료되면 지식을 응용 프로그램 컨텍스트로 통합할 수 있습니다. 프로토콜 오케스트레이션 페이지에서 컨텍스트 설명을 찾을 수 있습니다.",
                        style=me.Style(color="gray"),
                    )


def go_to_step(step_number: int):
    state = me.state(State)
    state.step = step_number


@me.component
def snackbar(
    *,
    is_visible: bool,
    label: str,
    action_label: str | None = None,
    on_click_action: Callable | None = None,
    horizontal_position: Literal["start", "center", "end"] = "center",
    vertical_position: Literal["start", "center", "end"] = "end",
):
    with me.box(
        style=me.Style(
            display="block" if is_visible else "none",
            height="100%",
            overflow_x="auto",
            overflow_y="auto",
            position="fixed",
            width="100%",
            z_index=1000,
        )
    ):
        with me.box(
            style=me.Style(
                align_items=vertical_position,
                height="100%",
                display="flex",
                justify_content=horizontal_position,
            )
        ):
            with me.box(
                style=me.Style(
                    align_items="center",
                    background=me.theme_var("on-surface-variant"),
                    border_radius=5,
                    box_shadow=(
                        "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
                    ),
                    display="flex",
                    font_size=14,
                    justify_content="space-between",
                    margin=me.Margin.all(10),
                    padding=(
                        me.Padding(top=5, bottom=5, right=5, left=15)
                        if action_label
                        else me.Padding.all(15)
                    ),
                    width=300,
                )
            ):
                me.text(
                    label,
                    style=me.Style(color=me.theme_var("surface-container-lowest")),
                )
                if action_label:
                    me.button(
                        action_label,
                        on_click=on_click_action,
                        style=me.Style(color=me.theme_var("primary-container")),
                    )
