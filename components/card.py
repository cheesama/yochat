import mesop as me

def card_component(
    title="Title",
    description="This is the Description",
    button_text="Get Started",
    path=None,
):
    with me.box(
        style=me.Style(
            flex_direction="column",
            display="flex",
            justify_content="space-between",
            gap=8,
            height=180,
            width=240,
            padding=me.Padding.all(16),
            border_radius=8,
            border=me.Border.symmetric(
                horizontal=me.BorderSide(
                    width=1, style="solid", color="primary"
                ),
                vertical=me.BorderSide(width=1, style="solid", color="primary"),
            ),
        ),
    ):
        me.text(
            title,
            style=me.Style(color="primary", font_weight=500, font_size=20),
        )
        me.text(description, type="subtitle-2")

        def redirect(e):
            print(title)
            print(path)
            if path:
                me.navigate(path)

        me.button(
            button_text,
            on_click=redirect,
            type="flat",
            style=me.Style(
                width="100%",
                border_radius=8,
                background="primary",
            ),
        )