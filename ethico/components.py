import reflex as rx 

from ethico import style
from ethico.state import State
from ethico.constants import INTRO_MESSAGE
from ethico.auth_state import AuthState

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, **style.sidebar_link_text),
            **style.sidebar_link_row,
        ),
        href=href,
        **style.sidebar_link_style,
    )



def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Chat", "message_circle", "/"),
        sidebar_item("Dilemmas", "scale", "/dilemmas"),
        sidebar_item("About", "info", "/about"),
        **style.sidebar_navigation,
    )



def sidebar_conversations() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("Recent conversations", **style.sidebar_conversations_heading),
            rx.spacer(),
            rx.button(
                rx.icon("square-pen", size=16),
                on_click=State.new_conversation,
                disabled=State.processing,
                aria_label="New conversation",
                title="New conversation",
                **style.sidebar_new_conversation_button,
            ),
            width="100%",
            align="center",
        ),
        rx.box(
            rx.vstack(
                rx.cond(
                    State.conversations.length() == 0,
                    rx.text("No conversations yet", **style.sidebar_conversations_empty),
                ),
                rx.foreach(
                    State.conversations,
                    lambda conversation: rx.button(
                        rx.text(conversation["title"], **style.sidebar_conversation_title),
                        on_click=lambda: State.open_conversation(conversation["id"]),
                        disabled=State.processing,
                        bg=rx.cond(
                            State.conversation_id == conversation["id"],
                            style.HOVER,
                            "transparent",
                        ),
                        **style.sidebar_conversation_item,
                    ),
                ),
                **style.sidebar_conversations_list,
            ),
            **style.sidebar_conversations_scroll,
        ),
        on_mount=State.load_conversations,
        **style.sidebar_conversations_section,
    )



def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("heart", **style.sidebar_logo),
            rx.heading(
                "THUFIR",
                **style.sidebar_heading,
            ),
            **style.sidebar_brand_row,
        ),

        sidebar_items(),
        rx.cond(
            AuthState.is_authenticated,
            sidebar_conversations(),
            rx.box(**style.sidebar_conversations_section),
        ),

        rx.vstack(
            rx.cond(
                AuthState.is_authenticated,
                rx.button(
                    rx.icon("log-out"),
                    rx.text("Log out", size="4"),
                    on_click=AuthState.sign_out,
                    **style.sidebar_logout,
                ),
                sidebar_item(
                    "Log in",
                    "log-in",
                    "/login",
                ),
            ),

            rx.divider(),

            rx.cond(
                AuthState.is_authenticated,
                rx.hstack(
                    rx.icon(
                        "user",
                        size=24,
                    ),
                    rx.vstack(
                        rx.text(
                            "My account",
                            **style.sidebar_account_title,
                        ),
                        rx.text(
                            AuthState.user_email,
                            **style.sidebar_account_email,
                        ),
                        **style.sidebar_account_info,
                    ),
                    **style.sidebar_account_row,
                ),
            ),

            **style.sidebar_footer,
        ),

        **style.sidebar_container,
    )

def qa(question: str, answer: str) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.markdown(question),
            **style.question_style,
        ),
        rx.box(
            rx.markdown(answer),
            **style.answer_style,
        ),
        **style.message_stack,
    )

def chat() -> rx.Component:
    return rx.box(
        rx.auto_scroll(
            rx.cond(
                State.chat_history.length() == 0, # type: ignore
                rx.box(
                    rx.markdown(INTRO_MESSAGE),
                    **style.intro_message,
                ),
            ),
            rx.foreach(
                State.chat_history,
                lambda messages: qa(messages[0], messages[1]),
            ),
            **style.chat_scroll,
        ),
        **style.chat_panel,
    )
    

def action_bar() -> rx.Component:
    enabled = AuthState.auth_checked & AuthState.is_authenticated
    return rx.vstack(
        rx.hstack(
            rx.input(
                value=State.question,
                disabled=State.processing | ~enabled,
                placeholder="Ask a question",
                on_change=State.set_question,
                style=style.input_style,
            ),
            rx.button(
                rx.icon("arrow-up", size=19),
                aria_label="Send message",
                on_click=State.answer,
                disabled=~enabled,
                loading=State.processing,
                style=style.button_style,
            ),
            **style.action_bar_row,
        ),
        **style.action_bar_container,
    )


def chat_page() -> rx.Component:
    """Shared layout for the main chat and dilemmas pages."""
    return rx.hstack(
        sidebar(),
        rx.center(
            rx.vstack(
                rx.cond(
                    (State.dilemma_json != "") & ~State.dilemma_panel_open,
                    rx.hstack(
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("chevron-left", size=18),
                            on_click=State.toggle_dilemma_panel,
                            aria_label="Open dilemma model",
                            title="Open dilemma model",
                            **style.dilemma_panel_toggle,
                        ),
                        width="100%",
                    ),
                ),
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
            (State.dilemma_json != "") & State.dilemma_panel_open,
            dilemma_panel(),
        ),
        **style.page_shell,
    )


def dilemma_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Dilemma model", size="4"),
            rx.spacer(),
            rx.icon_button(
                rx.icon("chevron-right", size=18),
                on_click=State.toggle_dilemma_panel,
                aria_label="Close dilemma model",
                title="Close dilemma model",
                **style.dilemma_panel_close,
            ),
            **style.dilemma_panel_header,
        ),
        rx.box(
            rx.code_block(State.dilemma_json, language="json"),
            **style.dilemma_panel_json,
        ),
        **style.dilemma_side_panel,
    )
