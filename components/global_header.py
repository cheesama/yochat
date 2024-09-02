import mesop as me


@me.component
def global_header_component():
    with me.box(
        style=me.Style(
            display="flex",
            justify_content="space-between",
            align_items="center",
            padding=me.Padding.all(16),
            background="#f1f5f9",
            border=me.Border(bottom=me.BorderSide(width=1, color="#e0e0e0")),
        )
    ):
        # 좌측 로고 및 이름
        with me.box(
            style=me.Style(display="flex", align_items="center"),
            on_click=lambda _: me.navigate("/chat"),
        ):
            me.icon(icon="home")  # 아이콘은 필요에 따라 변경 가능

        # 중앙 네비게이션
        with me.box(style=me.Style(display="flex", gap=20)):
            with me.tooltip(message="Prompt 등록 및 관리"):
                me.button("Prompts", on_click=lambda _: me.navigate("/prompt"))
            with me.tooltip(message="Document 등록 및 관리"):
                me.button(
                    "Document Store",
                    on_click=lambda _: me.navigate("/document_store"),
                )
            with me.tooltip(message="Tool 등록 및 관리"):
                me.button(
                    "Custom Tools", on_click=lambda _: me.navigate("/custom_tool")
                )
            with me.tooltip(message="API 등록 및 관리"):
                me.button("APIs", on_click=lambda _: me.navigate("/api"))

        # 우측 사용자 프로필
        with me.box(style=me.Style(display="flex", gap=20)):
            pass
            # me.text("cheehoon lee", style=me.Style(font_size=16))
