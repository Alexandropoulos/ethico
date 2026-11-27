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

page_shell = {
    "width": "100%",
    "height": "100dvh",
    "spacing": "0",
    "align": "stretch",
    "overflow": "hidden",
    "bg": BG,
}
page_content = {
    "flex": "1",
    "min_width": "0",
    "margin_left": SIDEBAR_WIDTH,
    "height": "100dvh",
    "overflow": "hidden",
}
chat_column = {
    "width": "100%",
    "max_width": CHAT_MAX_WIDTH,
    "height": "100%",
    "min_height": "0",
    "padding": "1.25rem",
    "spacing": "0",
    "align": "stretch",
}
error_text = {"color": rx.color("red", 11), "size": "2"}

# Navigation: quiet neutral sidebar, no colored accent.
sidebar_container = {
    "spacing": "5",
    "padding_x": "0.85rem",
    "padding_y": "1.4rem",
    "bg": SIDEBAR_BG,
    "align": "stretch",
    "position": "fixed",
    "top": "0",
    "left": "0",
    "height": "100dvh",
    "width": SIDEBAR_WIDTH,
    "overflow": "hidden",
    "z_index": "10",
    "border_right": f"1px solid {BORDER}",
}
sidebar_brand_row = {
    "align": "center",
    "justify": "start",
    "padding_x": "0.65rem",
    "width": "100%",
    "spacing": "3",
}
sidebar_heading = {
    "as_": "h2",
    "size": "5",
    "weight": "bold",
    "letter_spacing": "-0.025em",
}
sidebar_subheading = {
    "as_": "h3",
    "size": "2",
    "weight": "medium",
    "color": MUTED,
    "letter_spacing": "-0.025em",
}
sidebar_navigation = {"spacing": "1", "width": "100%"}
sidebar_link_style = {
    "underline": "none",
    "weight": "medium",
    "width": "100%",
    "color": TEXT,
}
sidebar_link_row = {
    "width": "100%",
    "padding_x": "0.75rem",
    "padding_y": "0.7rem",
    "align": "center",
    "spacing": "3",
    "border_radius": RADIUS_SMALL,
    "_hover": {"bg": HOVER},
}
sidebar_link_text = {"size": "3"}
sidebar_conversations_section = {
    "width": "100%",
    "flex": "1",
    "min_height": "0",
    "spacing": "2",
    "align": "stretch",
}
sidebar_conversations_heading = {
    "size": "2",
    "weight": "medium",
    "color": TEXT,
    "padding_x": "0.75rem",
}
sidebar_conversations_header = {"width": "100%", "align": "center"}
sidebar_new_conversation_button = {
    "variant": "ghost",
    "color_scheme": "gray",
    "size": "1",
    "padding": "0.4rem",
}
sidebar_conversations_scroll = {
    "width": "100%",
    "flex": "1",
    "min_height": "0",
    "overflow_y": "auto",
    "overflow_x": "hidden",
}
sidebar_conversations_list = {
    "width": "100%",
    "max_width": "100%",
    "spacing": "1",
    "align": "stretch",
}
sidebar_conversation_item = {
    "variant": "ghost",
    "color_scheme": "gray",
    "width": "100%",
    "max_width": "100%",
    "min_width": "0",
    "height": "36px",
    "padding_x": "0.75rem",
    "justify_content": "flex-start",
    "text_align": "left",
    "border_radius": RADIUS_SMALL,
    "cursor": "pointer",
    "overflow": "hidden",
    "flex_shrink": "0",
    "_hover": {"bg": HOVER},
}
sidebar_conversation_title_scroll = dict(
    width="100%",
    min_width="0",
    overflow="hidden",
    **{
        "&:hover .conversation-title": {
            "animation": "title-scroll 3s linear infinite alternate",
        },
        "@keyframes title-scroll": {
            "0%, 15%": {"transform": "translateX(0)"},
            "85%, 100%": {"transform": "translateX(min(0px, calc(180px - 100%)))"},
        },
    },
)

sidebar_conversation_title = {
    "class_name": "conversation-title",
    "size": "2",
    "color": TEXT,
    "white_space": "nowrap",
    "width": "max-content",
    "min_width": "100%",
    "text_align": "left",
}
sidebar_conversation_title_viewport = {
    "width": "100%",
    "min_width": "0",
    "overflow_x": "auto",
    "overflow_y": "hidden",
    "scrollbar_width": "thin",
}
sidebar_conversations_empty = {"size": "2", "color": MUTED, "padding": "0.75rem"}
sidebar_footer = {"width": "100%", "spacing": "4"}
sidebar_logout = {
    "variant": "ghost",
    "color_scheme": "gray",
    "width": "100%",
    "justify": "start",
}
sidebar_account_row = {
    "padding_x": "0.5rem",
    "align": "center",
    "justify": "start",
    "width": "100%",
}
sidebar_account_info = {"spacing": "0", "align": "start", "width": "100%"}
sidebar_account_title = {"size": "3", "weight": "bold"}
sidebar_account_email = {
    "size": "2",
    "weight": "medium",
    "color": MUTED,
    "overflow_wrap": "anywhere",
}

# Borderless conversation canvas. Only user messages get a quiet bubble.
message_stack = {
    "width": "100%",
    "spacing": "4",
    "align": "stretch",
    "margin_y": "0.65rem",
}
message_base = {
    "padding": "0.85rem 1.1rem",
    "border_radius": RADIUS_MESSAGE,
    "max_width": MESSAGE_MAX_WIDTH,
    "overflow_wrap": "anywhere",
    "line_height": "1.65",
}
question_style = message_base | {"bg": SURFACE, "align_self": "end"}
answer_style = message_base | {
    "bg": "transparent",
    "align_self": "start",
    "padding_x": "0.25rem",
    "max_width": "100%",
}
intro_message = {
    "padding": "1.2rem 0.25rem",
    "bg": "transparent",
    "align_self": "start",
    "max_width": "100%",
    "color": TEXT,
    "line_height": "1.7",
}
chat_panel = {
    "width": "100%",
    "flex": "1",
    "min_height": "0",
    "bg": "transparent",
    "overflow": "hidden",
}
chat_scroll = {
    "width": "100%",
    "height": "100%",
    "min_height": "0",
    "padding": "1.2rem 0.65rem",
}

# A single floating composer, with an icon-only submit action.
action_bar_container = {
    "width": "100%",
    "spacing": "2",
    "padding_top": "0.65rem",
    "padding_bottom": "0.4rem",
}
action_bar_row = dict(
    width="100%",
    align="center",
    spacing="2",
    padding="0.45rem",
    bg=SURFACE,
    border=f"1px solid {BORDER}",
    border_radius=RADIUS_COMPOSER,
    _focus_within={
        "border_color": BORDER,
        "box_shadow": "none",
    },
    **{
        "&:has(input:disabled)": {
            "background_color": SURFACE,
            "opacity": "1",
        },
    },
)
input_style = dict(
    width="100%",
    min_width="0",
    flex="1",
    height=CONTROL_HEIGHT,
    border="none",
    background_color="transparent",
    box_shadow="none",
    opacity="1",
    color=TEXT,
    **{
        "& input": {
            "padding": "0 12px",
            "font_size": "15px",
            "border": "none",
            "outline": "none",
            "box_shadow": "none",
            "background": "transparent",
            "opacity": "1",
        },
        "& input:disabled": {
            "background": "transparent",
            "background_color": "transparent",
            "opacity": "1",
            "color": TEXT,
            "cursor": "not-allowed",
        },
        "&[data-disabled]": {
            "background": "transparent",
            "opacity": "1",
        },
        "& input::placeholder": {
            "color": MUTED,
            "opacity": "1",
        },
        "&:focus-within": {
            "outline": "none",
            "box_shadow": "none",
            "background": "transparent",
        },
    },
)
button_style = {
    "flex_shrink": "0",
    "width": "38px",
    "height": "38px",
    "padding": "0",
    "border_radius": "12px",
    "background_color": TEXT,
    "color": BG,
    "cursor": "pointer",
    "_hover": {"opacity": "0.8"},
    "_disabled": {"opacity": "0.4", "cursor": "not-allowed"},
}
composer_hint = {"size": "1", "color": MUTED, "text_align": "center"}

# Informational pages
about_page_content = {
    "margin_left": SIDEBAR_WIDTH,
    "width": "100%",
    "min_height": "100dvh",
    "overflow_y": "auto",
    "bg": BG,
}
about_page_center = {"width": "100%", "padding": "2.5rem"}
about_page_shell = {"width": "100%", "align": "start", "spacing": "0"}
about_card = {
    "width": "100%",
    "max_width": CONTENT_MAX_WIDTH,
    "padding": "1.5rem",
    "bg": "transparent",
}
about_stack = {"spacing": "5", "align": "stretch", "width": "100%"}
about_heading = {"size": "8", "weight": "bold"}

# Authentication
login_page = {"height": "100dvh", "bg": BG}
login_card = {
    "bg": SIDEBAR_BG,
    "border": f"1px solid {BORDER}",
    "border_radius": RADIUS_COMPOSER,
    "padding": "1.5rem",
}
login_stack = {"spacing": "4", "width": "300px"}
login_heading = {"size": "7"}
login_input = {"width": "100%", "color_scheme": "gray"}
login_button = {"width": "100%", "color_scheme": "gray", "high_contrast": True}
login_secondary_button = {"variant": "outline", "color_scheme": "gray", "width": "100%"}
login_error = {"color": rx.color("red", 11)}

# Dilemmas page: compact two-panel library; all style choices live here.
dilemma_panels = {
    "flex": "1",
    "margin_left": SIDEBAR_WIDTH,
    "height": "100dvh",
    "min_width": "0",
    "align": "stretch",
    "spacing": "0",
    "overflow": "hidden",
}
dilemma_list_panel = {
    "width": "22rem",
    "flex_shrink": "0",
    "height": "100%",
    "min_height": "0",
    "padding": "1.5rem 1rem",
    "align": "stretch",
    "spacing": "4",
    "overflow_y": "auto",
    "bg": SIDEBAR_BG,
    "border_right": f"1px solid {BORDER}",
}
dilemma_page_heading = {"size": "6", "weight": "bold"}
dilemma_search = {"width": "100%", "color_scheme": "gray", "variant": "surface"}
dilemma_items = {"spacing": "2", "align": "stretch", "width": "100%"}
dilemma_item = {
    "width": "100%",
    "height": "auto",
    "padding": "0.85rem",
    "justify": "start",
    "white_space": "normal",
    "text_align": "left",
    "color": TEXT,
    "border_radius": RADIUS_SMALL,
    "cursor": "pointer",
    "variant": "ghost",
    "_hover": {"bg": HOVER},
}
dilemma_item_title = {"weight": "medium", "size": "3", "overflow_wrap": "anywhere"}
dilemma_item_description = dict(
    size="2",
    color=MUTED,
    overflow="hidden",
    display="-webkit-box",
    **{"-webkit-line-clamp": "2", "-webkit-box-orient": "vertical"},
)
dilemma_item_date = {"size": "1", "color": MUTED}
dilemma_detail_panel = {
    "flex": "1",
    "min_width": "0",
    "height": "100%",
    "padding": "1.5rem 2rem",
    "overflow_y": "auto",
    "bg": BG,
}
dilemma_detail_body = {
    "spacing": "6",
    "align": "stretch",
    "width": "100%",
    "max_width": "65rem",
    "margin_x": "auto",
    "padding_bottom": "3rem",
}
dilemma_detail_header = {
    "width": "100%",
    "align": "start",
    "justify": "between",
    "spacing": "3",
}
dilemma_title = {"size": "7", "weight": "bold", "overflow_wrap": "anywhere"}
dilemma_open_button = {"variant": "outline", "color_scheme": "gray", "flex_shrink": "0"}
dilemma_section = {
    "spacing": "3",
    "align": "stretch",
    "width": "100%",
    "border_top": f"1px solid {BORDER}",
    "padding_top": "1.25rem",
}
dilemma_section_heading = {"size": "4", "weight": "bold"}
dilemma_description = {
    "size": "3",
    "line_height": "1.75",
    "color": TEXT,
    "overflow_wrap": "anywhere",
}
dilemma_field = {"spacing": "2", "align": "stretch", "width": "100%"}
dilemma_field_label = {"size": "2", "weight": "medium", "color": MUTED}
dilemma_chip = {
    "size": "2",
    "padding": "0.35rem 0.6rem",
    "bg": SURFACE,
    "border_radius": "7px",
    "font_family": "monospace",
    "overflow_wrap": "anywhere",
}
dilemma_map = {
    "spacing": "0",
    "width": "100%",
    "align": "stretch",
    "border": f"1px solid {BORDER}",
    "border_radius": RADIUS_SMALL,
    "overflow": "hidden",
}
dilemma_map_row = {
    "spacing": "1",
    "width": "100%",
    "padding": "0.75rem",
    "align": "stretch",
    "border_bottom": f"1px solid {BORDER}",
}
dilemma_map_key = {
    "font_family": "monospace",
    "size": "2",
    "weight": "medium",
    "color": TEXT,
    "overflow_wrap": "anywhere",
}
dilemma_map_value = {
    "font_family": "monospace",
    "size": "2",
    "white_space": "pre-wrap",
    "color": MUTED,
    "overflow_wrap": "anywhere",
}
dilemma_empty_field = {"color": MUTED, "size": "2"}
dilemma_placeholder = {"color": MUTED, "size": "3", "padding": "1rem"}

# Right-side dilemma model inspector
dilemma_side_panel = {
    "width": "26rem",
    "max_width": "38vw",
    "flex_shrink": "0",
    "height": "100dvh",
    "min_height": "0",
    "spacing": "0",
    "align": "stretch",
    "bg": SIDEBAR_BG,
    "border_left": f"1px solid {BORDER}",
    "overflow": "hidden",
}
dilemma_panel_header = {
    "width": "100%",
    "align": "center",
    "padding": "1rem 1.25rem",
    "border_bottom": f"1px solid {BORDER}",
}
dilemma_panel_close = {"variant": "ghost", "color_scheme": "gray", "size": "2"}
dilemma_panel_json = {
    "width": "100%",
    "flex": "1",
    "min_height": "0",
    "overflow": "auto",
    "padding": "1rem",
}
dilemma_panel_toggle = {
    "position": "fixed",
    "top": "1rem",
    "right": "1.25rem",
    "z_index": "20",
    "variant": "soft",
    "color_scheme": "gray",
    "size": "2",
    "cursor": "pointer",
}
