import reflex as rx

NEUTRAL = "slate"
SIDEBAR_WIDTH = "15rem"
CHAT_MAX_WIDTH = "52rem"
CONTENT_MAX_WIDTH = "52rem"
MESSAGE_MAX_WIDTH = "82%"
RADIUS_SMALL = "10px"
RADIUS_MESSAGE = "18px"
RADIUS_COMPOSER = "22px"
CONTROL_HEIGHT = "44px"

BG = rx.color(NEUTRAL, 1)
SIDEBAR_BG = rx.color(NEUTRAL, 2)
SURFACE = rx.color(NEUTRAL, 3)
HOVER = rx.color(NEUTRAL, 4)
BORDER = rx.color(NEUTRAL, 6)
TEXT = rx.color(NEUTRAL, 12)
MUTED = rx.color(NEUTRAL, 11)

page_shell = dict(width="100%", height="100dvh", spacing="0", align="stretch", overflow="hidden", bg=BG)
page_content = dict(flex="1", min_width="0", margin_left=SIDEBAR_WIDTH, height="100dvh", overflow="hidden")
chat_column = dict(width="100%", max_width=CHAT_MAX_WIDTH, height="100%", min_height="0", padding="1.25rem", spacing="0", align="stretch")
error_text = dict(color=rx.color("red", 11), size="2")

# Navigation: quiet neutral sidebar, no colored accent.
sidebar_container = dict(spacing="5", padding_x="0.85rem", padding_y="1.4rem", bg=SIDEBAR_BG,
    align="stretch", position="fixed", top="0", left="0", height="100dvh",
    width=SIDEBAR_WIDTH, overflow="hidden", z_index="10", border_right=f"1px solid {BORDER}")
sidebar_brand_row = dict(align="center", justify="start", padding_x="0.65rem", width="100%", spacing="3")
sidebar_logo = dict(size=23, color=TEXT)
sidebar_heading = dict(as_="h2", size="5", weight="bold", letter_spacing="-0.025em")
sidebar_navigation = dict(spacing="1", width="100%")
sidebar_link_style = dict(underline="none", weight="medium", width="100%", color=TEXT)
sidebar_link_row = dict(width="100%", padding_x="0.75rem", padding_y="0.7rem", align="center", spacing="3",
    border_radius=RADIUS_SMALL, _hover={"bg": HOVER})
sidebar_link_text = dict(size="3")
sidebar_conversations_section = dict(width="100%", flex="1", min_height="0", spacing="2", align="stretch")
sidebar_conversations_heading = dict(size="2", weight="medium", color=MUTED, padding_x="0.75rem")
sidebar_new_conversation_button = dict(variant="ghost", color_scheme="gray", size="1", padding="0.4rem")
sidebar_conversations_scroll = dict(width="100%", flex="1", min_height="0", overflow_y="auto", overflow_x="hidden")
sidebar_conversations_list = dict(width="100%", max_width="100%", spacing="1", align="stretch")
sidebar_conversation_item = dict(
    variant="ghost", color_scheme="gray", width="100%", max_width="100%", min_width="0",
    height="36px", padding_x="0.75rem", justify_content="flex-start", text_align="left",
    border_radius=RADIUS_SMALL, cursor="pointer", overflow="hidden", flex_shrink="0",
    _hover={"bg": HOVER},
)
sidebar_conversation_title = dict(
    size="2", color=TEXT, width="100%", min_width="0", text_align="left",
    overflow="hidden", text_overflow="ellipsis", white_space="nowrap",
)
sidebar_conversations_empty = dict(size="2", color=MUTED, padding="0.75rem")
sidebar_footer = dict(width="100%", spacing="4")
sidebar_logout = dict(variant="ghost", color_scheme="gray", width="100%", justify="start")
sidebar_account_row = dict(padding_x="0.5rem", align="center", justify="start", width="100%")
sidebar_account_info = dict(spacing="0", align="start", width="100%")
sidebar_account_title = dict(size="3", weight="bold")
sidebar_account_email = dict(size="2", weight="medium", color=MUTED, overflow_wrap="anywhere")

# Borderless conversation canvas. Only user messages get a quiet bubble.
message_stack = dict(width="100%", spacing="4", align="stretch", margin_y="0.65rem")
message_base = dict(padding="0.85rem 1.1rem", border_radius=RADIUS_MESSAGE,
    max_width=MESSAGE_MAX_WIDTH, overflow_wrap="anywhere", line_height="1.65")
question_style = message_base | dict(bg=SURFACE, align_self="end")
answer_style = message_base | dict(bg="transparent", align_self="start", padding_x="0.25rem", max_width="100%")
intro_message = dict(padding="1.2rem 0.25rem", bg="transparent", align_self="start",
    max_width="100%", color=TEXT, line_height="1.7")
chat_panel = dict(width="100%", flex="1", min_height="0", bg="transparent", overflow="hidden")
chat_scroll = dict(width="100%", height="100%", min_height="0", padding="1.2rem 0.65rem")

# A single floating composer, with an icon-only submit action.
action_bar_container = dict(width="100%", spacing="2", padding_top="0.65rem", padding_bottom="0.4rem")
action_bar_row = dict(width="100%", align="center", spacing="2", padding="0.45rem",
    bg=SURFACE, border=f"1px solid {BORDER}", border_radius=RADIUS_COMPOSER)
input_style = dict(width="100%", min_width="0", flex="1", height=CONTROL_HEIGHT,
    border="none", background_color="transparent", box_shadow="none",
    **{"& input": {"padding": "0 12px", "font_size": "15px", "border": "none",
                   "outline": "none", "box_shadow": "none", "background": "transparent"},
       "& input::placeholder": {"color": MUTED},
       "&:focus-within": {"outline": "none", "box_shadow": "none", "background": "transparent"}})
button_style = dict(flex_shrink="0", width="38px", height="38px", padding="0",
    border_radius="12px", background_color=TEXT, color=BG, cursor="pointer",
    _hover={"opacity": "0.8"}, _disabled={"opacity": "0.4", "cursor": "not-allowed"})
composer_hint = dict(size="1", color=MUTED, text_align="center")

# Informational pages
about_page_content = dict(margin_left=SIDEBAR_WIDTH, width="100%", min_height="100dvh", overflow_y="auto", bg=BG)
about_page_center = dict(width="100%", padding="2.5rem")
about_page_shell = dict(width="100%", align="start", spacing="0")
about_card = dict(width="100%", max_width=CONTENT_MAX_WIDTH, padding="1.5rem", bg="transparent")
about_stack = dict(spacing="5", align="stretch", width="100%")
about_heading = dict(size="8", weight="bold")

# Authentication
login_page = dict(height="100dvh", bg=BG)
login_card = dict(bg=SIDEBAR_BG, border=f"1px solid {BORDER}", border_radius=RADIUS_COMPOSER, padding="1.5rem")
login_stack = dict(spacing="4", width="300px")
login_heading = dict(size="7")
login_input = dict(width="100%", color_scheme="gray")
login_button = dict(width="100%", color_scheme="gray", high_contrast=True)
login_secondary_button = dict(variant="outline", color_scheme="gray", width="100%")
login_error = dict(color=rx.color("red", 11))

# Dilemmas page: compact two-panel library; all style choices live here.
dilemma_panels = dict(
    flex="1", margin_left=SIDEBAR_WIDTH, height="100dvh", min_width="0",
    align="stretch", spacing="0", overflow="hidden",
)
dilemma_list_panel = dict(
    width="22rem", flex_shrink="0", height="100%", min_height="0",
    padding="1.5rem 1rem", align="stretch", spacing="4",
    overflow_y="auto", bg=SIDEBAR_BG, border_right=f"1px solid {BORDER}",
)
dilemma_page_heading = dict(size="6", weight="bold")
dilemma_search = dict(width="100%", color_scheme="gray", variant="surface")
dilemma_items = dict(spacing="2", align="stretch", width="100%")
dilemma_item = dict(
    width="100%", height="auto", padding="0.85rem", justify="start",
    white_space="normal", text_align="left", color=TEXT,
    border_radius=RADIUS_SMALL, cursor="pointer", variant="ghost",
    _hover={"bg": HOVER},
)
dilemma_item_title = dict(weight="medium", size="3", overflow_wrap="anywhere")
dilemma_item_description = dict(
    size="2", color=MUTED, overflow="hidden", display="-webkit-box",
    **{"-webkit-line-clamp": "2", "-webkit-box-orient": "vertical"},
)
dilemma_item_date = dict(size="1", color=MUTED)
dilemma_detail_panel = dict(
    flex="1", min_width="0", height="100%", padding="1.5rem 2rem",
    overflow_y="auto", bg=BG,
)
dilemma_detail_body = dict(
    spacing="6", align="stretch", width="100%", max_width="65rem",
    margin_x="auto", padding_bottom="3rem",
)
dilemma_detail_header = dict(width="100%", align="start", justify="between", spacing="3")
dilemma_title = dict(size="7", weight="bold", overflow_wrap="anywhere")
dilemma_open_button = dict(variant="outline", color_scheme="gray", flex_shrink="0")
dilemma_section = dict(spacing="3", align="stretch", width="100%", border_top=f"1px solid {BORDER}", padding_top="1.25rem")
dilemma_section_heading = dict(size="4", weight="bold")
dilemma_description = dict(size="3", line_height="1.75", color=TEXT, overflow_wrap="anywhere")
dilemma_field = dict(spacing="2", align="stretch", width="100%")
dilemma_field_label = dict(size="2", weight="medium", color=MUTED)
dilemma_chip = dict(
    size="2", padding="0.35rem 0.6rem", bg=SURFACE,
    border_radius="7px", font_family="monospace", overflow_wrap="anywhere",
)
dilemma_map = dict(spacing="0", width="100%", align="stretch", border=f"1px solid {BORDER}", border_radius=RADIUS_SMALL, overflow="hidden")
dilemma_map_row = dict(spacing="1", width="100%", padding="0.75rem", align="stretch", border_bottom=f"1px solid {BORDER}")
dilemma_map_key = dict(font_family="monospace", size="2", weight="medium", color=TEXT, overflow_wrap="anywhere")
dilemma_map_value = dict(font_family="monospace", size="2", white_space="pre-wrap", color=MUTED, overflow_wrap="anywhere")
dilemma_empty_field = dict(color=MUTED, size="2")
dilemma_placeholder = dict(color=MUTED, size="3", padding="1rem")
# Right-side dilemma model inspector
dilemma_side_panel = dict(
    width="26rem", max_width="38vw", flex_shrink="0", height="100dvh",
    min_height="0", spacing="0", align="stretch", bg=SIDEBAR_BG,
    border_left=f"1px solid {BORDER}", overflow="hidden",
)
dilemma_panel_header = dict(
    width="100%", align="center", padding="1rem 1.25rem",
    border_bottom=f"1px solid {BORDER}",
)
dilemma_panel_close = dict(variant="ghost", color_scheme="gray", size="2")
dilemma_panel_json = dict(
    width="100%", flex="1", min_height="0", overflow="auto",
    padding="1rem",
)
dilemma_panel_toggle = dict(variant="ghost", color_scheme="gray", size="2")
