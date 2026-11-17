import asyncio
import json
import logging
from datetime import datetime
from typing import Any

import reflex as rx

from ethico import style
from ethico.auth_state import AuthState
from ethico.components import sidebar

logger = logging.getLogger(__name__)
PAGE_SIZE = 500


def _date_label(iso_date: str) -> str:
    try:
        return datetime.fromisoformat(iso_date.replace("Z", "+00:00")).strftime(
            "%d %b %Y"
        )
    except (ValueError, AttributeError):
        return iso_date or ""


def _value_text(value: Any) -> str:
    """Preserve JSON notation for non-string values (including nested affects)."""
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def _pairs(value: Any) -> list[dict[str, str]]:
    """Display every key and value without interpreting HERA expressions."""
    if not isinstance(value, dict):
        return [{"key": "Value", "value": _value_text(value)}]
    return [
        {"key": str(key), "value": _value_text(item)} for key, item in value.items()
    ]


class DilemmasState(rx.State):
    """Page state; kept here rather than adding separate state/service files."""

    dilemmas: list[dict[str, str]] = []
    formulations: dict[str, dict] = {}
    search: str = ""
    selected_id: str = ""
    selected_title: str = ""
    selected_date: str = ""
    description: str = ""
    actions: list[str] = []
    patients: list[str] = []
    consequences: list[str] = []
    mechanisms: list[dict[str, str]] = []
    utilities: list[dict[str, str]] = []
    goals: list[dict[str, str]] = []
    affects: list[dict[str, str]] = []
    loading: bool = False
    error: str = ""
    loaded_user_id: str = ""

    @rx.var
    def filtered_dilemmas(self) -> list[dict[str, str]]:
        query = self.search.strip().casefold()
        if not query:
            return self.dilemmas
        return [
            d
            for d in self.dilemmas
            if query in d["title"].casefold() or query in d["description"].casefold()
        ]

    def _select(self, conversation_id: str):
        record = self.formulations.get(conversation_id)
        if record is None:
            return
        dilemma = record["dilemma"]
        self.selected_id = conversation_id
        self.selected_title = record["title"]
        self.selected_date = record["date"]
        self.description = str(dilemma.get("description", ""))
        self.actions = list(dilemma.get("actions") or [])
        self.patients = list(dilemma.get("patients") or [])
        self.consequences = list(dilemma.get("consequences") or [])
        self.mechanisms = _pairs(dilemma.get("mechanisms", {}))
        self.utilities = _pairs(dilemma.get("utilities", {}))
        self.goals = _pairs(dilemma.get("goals", {}))
        self.affects = _pairs(dilemma.get("affects", {}))

    @rx.event
    def select_dilemma(self, conversation_id: str):
        self._select(conversation_id)

    @rx.event
    def set_search(self, value: str):
        self.search = value

    @rx.event
    async def load_dilemmas(self):
        # Clear any previously displayed account's data before the fetch.
        self.dilemmas = []
        self.formulations = {}
        self.selected_id = ""
        self.selected_title = ""
        self.selected_date = ""
        self.description = ""
        self.actions = []
        self.patients = []
        self.consequences = []
        self.mechanisms = []
        self.utilities = []
        self.goals = []
        self.affects = []
        self.error = ""
        self.loaded_user_id = ""
        self.loading = True
        yield

        try:
            auth = await self.get_state(AuthState)
            client = auth._authenticated_client()
            user_id = (
                auth.user_id
            )  # Verified against Supabase by _authenticated_client.

            # Fetch all qualifying conversations, not just Supabase's first page.
            # We never select the `evaluation` JSON itself: it is only a filter.
            def fetch_rows():
                result = []
                offset = 0
                while True:
                    response = (
                        client.table("conversations")
                        .select("id,title,created_at,dilemma")
                        .eq("user_id", user_id)
                        .not_.is_("dilemma", "null")
                        .not_.is_("evaluation", "null")
                        .order("created_at", desc=True)
                        .range(offset, offset + PAGE_SIZE - 1)
                        .execute()
                    )
                    batch = response.data or []
                    result.extend(batch)
                    if len(batch) < PAGE_SIZE:
                        break
                    offset += PAGE_SIZE
                return result

            rows = await asyncio.to_thread(fetch_rows)
            previews = []
            formulations = {}
            for row in rows:
                dilemma = row.get("dilemma")
                if not isinstance(dilemma, dict):
                    continue
                conversation_id = str(row["id"])
                title = row.get("title") or "New conversation"
                date = _date_label(row.get("created_at") or "")
                description = str(dilemma.get("description", ""))
                previews.append(
                    {
                        "id": conversation_id,
                        "title": title,
                        "description": description,
                        "date": date,
                    }
                )
                formulations[conversation_id] = {
                    "title": title,
                    "date": date,
                    "dilemma": dilemma,
                }

            self.dilemmas = previews
            self.formulations = formulations
            self.loaded_user_id = user_id
            if previews:
                self._select(previews[0]["id"])

        except PermissionError:
            self.error = "You must sign in to view your dilemmas."
            yield rx.redirect("/login")
            return
        except Exception:
            logger.exception("Failed to load saved dilemmas")
            self.error = "Could not load dilemmas. Please try again."
        finally:
            self.loading = False

    @rx.event
    def open_conversation(self):
        # Navigation intentionally not implemented yet.
        return rx.toast.info("Restoring conversations is not implemented yet.")


def _list_item(item: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.button(
        rx.vstack(
            rx.text(item["title"], **style.dilemma_item_title),
            rx.text(item["description"], **style.dilemma_item_description),
            rx.text(item["date"], **style.dilemma_item_date),
            spacing="1",
            align="start",
            width="100%",
        ),
        on_click=lambda: DilemmasState.select_dilemma(item["id"]),
        bg=rx.cond(
            DilemmasState.selected_id == item["id"], style.SURFACE, "transparent"
        ),
        **style.dilemma_item,
    )


def _section(title: str, *content: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.heading(title, **style.dilemma_section_heading),
        *content,
        **style.dilemma_section,
    )


def _terms(label: str, terms: rx.Var[list[str]]) -> rx.Component:
    return rx.vstack(
        rx.text(label, **style.dilemma_field_label),
        rx.cond(
            terms.length() > 0,
            rx.flex(
                rx.foreach(terms, lambda term: rx.text(term, **style.dilemma_chip)),
                wrap="wrap",
                gap="2",
                width="100%",
            ),
            rx.text("None", **style.dilemma_empty_field),
        ),
        **style.dilemma_field,
    )


def _mapping(label: str, pairs: rx.Var[list[dict[str, str]]]) -> rx.Component:
    return rx.vstack(
        rx.text(label, **style.dilemma_field_label),
        rx.cond(
            pairs.length() > 0,
            rx.vstack(
                rx.foreach(
                    pairs,
                    lambda pair: rx.vstack(
                        rx.text(pair["key"], **style.dilemma_map_key),
                        rx.text(pair["value"], **style.dilemma_map_value),
                        **style.dilemma_map_row,
                    ),
                ),
                **style.dilemma_map,
            ),
            rx.text("None", **style.dilemma_empty_field),
        ),
        **style.dilemma_field,
    )


def _details() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(DilemmasState.selected_title, **style.dilemma_title),
                rx.text(
                    "Conversation created ",
                    DilemmasState.selected_date,
                    **style.dilemma_item_date,
                ),
                spacing="1",
                align="start",
                flex="1",
                min_width="0",
            ),
            rx.button(
                rx.icon("message-circle", size=17),
                "Go to conversation",
                on_click=DilemmasState.open_conversation,
                **style.dilemma_open_button,
            ),
            **style.dilemma_detail_header,
        ),
        _section(
            "Situation", rx.text(DilemmasState.description, **style.dilemma_description)
        ),
        _section(
            "Elements",
            _terms("Actions", DilemmasState.actions),
            _terms("Patients", DilemmasState.patients),
            _terms("Consequences", DilemmasState.consequences),
        ),
        _section(
            "Causal structure",
            _mapping("Mechanisms", DilemmasState.mechanisms),
            _mapping("Goals", DilemmasState.goals),
        ),
        _section(
            "Ethical parameters",
            _mapping("Utilities", DilemmasState.utilities),
            _mapping("Affects", DilemmasState.affects),
        ),
        **style.dilemma_detail_body,
    )


def dilemmas() -> rx.Component:
    """Use your existing /dilemmas registration; see installation note."""
    return rx.hstack(
        sidebar(),
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading("Dilemmas", **style.dilemma_page_heading),
                    rx.spacer(),
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        on_click=DilemmasState.load_dilemmas,
                        aria_label="Refresh dilemmas",
                        variant="ghost",
                        color_scheme="gray",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.input(
                    placeholder="Search dilemmas",
                    value=DilemmasState.search,
                    on_change=DilemmasState.set_search,
                    **style.dilemma_search,
                ),
                rx.cond(
                    DilemmasState.loading,
                    rx.text("Loading dilemmas...", **style.dilemma_placeholder),
                    rx.cond(
                        DilemmasState.filtered_dilemmas.length() > 0,
                        rx.vstack(
                            rx.foreach(DilemmasState.filtered_dilemmas, _list_item),
                            **style.dilemma_items,
                        ),
                        rx.text("No dilemmas found.", **style.dilemma_placeholder),
                    ),
                ),
                **style.dilemma_list_panel,
            ),
            rx.box(
                rx.cond(
                    DilemmasState.error != "",
                    rx.text(DilemmasState.error, role="alert", **style.error_text),
                    rx.cond(
                        DilemmasState.selected_id != "",
                        _details(),
                        rx.text(
                            "Select a dilemma to view its formulation.",
                            **style.dilemma_placeholder,
                        ),
                    ),
                ),
                **style.dilemma_detail_panel,
            ),
            **style.dilemma_panels,
        ),
        on_mount=DilemmasState.load_dilemmas,
        **style.page_shell,
    )
