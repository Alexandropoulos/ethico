import reflex as rx

from ethico.state import State
from ethico.components import chat, sidebar, action_bar
from ethico import style    


def index() -> rx.Component:
        return rx.hstack(
        sidebar(),
        rx.center(
            rx.vstack(
                chat(),
                action_bar(),
                rx.cond(
                    State.error != "",
                    rx.text(State.error, role="alert", **style.error_text),
                ),
                **style.chat_column,
            ),
            **style.page_content,
        ),
        rx.cond(
            (State.dilemma_json != "") & ~State.dilemma_panel_open,
            rx.button(
                rx.icon("panel-right-open", size=17),
                "Show dilemma model",
                on_click=State.toggle_dilemma_panel,
                aria_label="Show dilemma model",
                **style.dilemma_panel_toggle,
            ),
        ),
        **style.page_shell,
    )

