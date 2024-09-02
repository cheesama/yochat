import mesop as me

from components.global_header import global_header_component
from components.card import card_component

@me.page(path="/api")
def api_list_page():
    global_header_component()

    cards = [
        {
            "title": "Templating",
            "description": "Generate documents from templates",
            "button_text": "Get Started",
            "path": "/templating",
        },
        {
            "title": "Parsing",
            "description": "Parse configuration files into a excel file",
            "button_text": "Convert",
            "path": "/parsing",
        },
        {
            "title": "Connectors",
            "description": "API Integration with other systems or vendors",
            "button_text": "Connect",
            "path": "/connectors",
        },
        {
            "title": "Stats",
            "description": "Utilization statistics on APP usage",
            "button_text": "View",
            "path": "/stats",
        },
        {
            "title": "Admin",
            "description": "Access to Administration Dashboard Panel",
            "button_text": "Administrate",
            "path": "/admin",
        },
    ]

    with me.box(
        style=me.Style(
            margin=me.Margin.symmetric(vertical="3%", horizontal="5%"),
        ),
    ):
        with me.box(
            style=me.Style(
                display="flex",
                flex_wrap="wrap",
                gap=16,
                border_radius=8,
            ),
        ):
            for card in cards:
                card_component(
                    title=card["title"],
                    description=card["description"],
                    button_text=card["button_text"],
                    path=card["path"],
                )
