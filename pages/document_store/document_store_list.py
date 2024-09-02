import mesop as me

from components.global_header import global_header_component


@me.page(
    path="/document_store",
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io", "https://huggingface.co"]
    ),
)
def document_store_list_page():
    # 글로벌 헤더 추가
    global_header_component()

    with me.box(style=me.Style(display="flex", gap="20px", padding=me.Padding.all(16))):
        # 지식 생성 버튼
        with me.box(
            style=me.Style(
                background="lightgray",
                padding=me.Padding.all(24),
                border_radius=8,
                width="25%",  # 고정 너비 사용
                display="flex",
                flex_direction="column",
                justify_content="center",
                align_items="center",
            ),
            on_click=lambda event: me.navigate("/document_store_create"),
        ):
            me.icon(icon="add")  # 올바른 아이콘 속성 사용
            me.text(
                "Document Store 생성",
                style=me.Style(
                    font_size=20, margin=me.Margin(top=10), font_weight="bold"
                ),
            )
            me.text(
                "자체 텍스트 데이터를 가져오거나 LLM 컨텍스트를 강화하기 위해 앱들을 통해 실시간 데이터를 기록할 수 있습니다.",
                style=me.Style(
                    text_align="center", margin=me.Margin(top=10), color="gray"
                ),
            )

        # 기존 데이터들
        for title in [
            "시스템 디자인 가이드",
            "사내 빅쿼리 가이드",
            "ByteByteGo-Big-Archive",
        ]:
            with me.box(
                style=me.Style(
                    background="white",
                    padding=me.Padding.all(16),
                    border=me.Border.all(
                        me.BorderSide(width=2, color="#e0e0e0", style="solid")
                    ),
                    border_radius=8,
                    width="25%",  # 고정 너비 사용
                )
            ):
                me.icon(icon="folder")  # 올바른 아이콘 속성 사용
                me.text(
                    title,
                    style=me.Style(
                        font_size=18, font_weight="bold", margin=me.Margin(top=10)
                    ),
                )
                me.text(
                    "useful for when you want to answer queries about the ByteByteGo-Big-Archive...",
                    style=me.Style(margin=me.Margin(top=5), color="gray"),
                )
