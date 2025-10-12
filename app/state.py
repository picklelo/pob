import reflex as rx
import os
import asyncio
import logging
import json
from notion_client import AsyncClient
from typing import TypedDict, Optional


class Poem(TypedDict):
    id: str
    title: str
    date: str
    image_url: Optional[str]
    excerpt: str
    content: list[str]


class PoetryState(rx.State):
    """Manages the state for the poetry collection app."""

    database_id: str = "6e09b54e-712e-495a-8dd9-835da66b0e40"
    poems: list[Poem] = []
    preamble_poem: Optional[Poem] = None
    is_loading: bool = True
    error_message: str = ""
    selected_poem: Optional[Poem] = None
    is_poem_loading: bool = False
    search_term: str = ""
    sort_by: str = "Recent"
    sort_options: list[str] = ["Recent", "Oldest First", "Title (A-Z)"]
    favorite_ids: list[str] = []
    idle: bool = False

    @rx.var
    def _sorted_poems(self) -> list[Poem]:
        """Returns poems sorted by date, which is the base for navigation."""
        return sorted(self.poems, key=lambda p: p.get("date", ""), reverse=True)

    @rx.var
    def current_poem_index(self) -> int:
        """Returns the index of the currently selected poem in the date-sorted list."""
        if not self.selected_poem or not self.selected_poem.get("id"):
            return -1
        try:
            poem_id = self.selected_poem["id"]
            return next(
                (i for i, p in enumerate(self._sorted_poems) if p["id"] == poem_id), -1
            )
        except (ValueError, KeyError) as e:
            logging.exception(f"Error finding poem index: {e}")
            return -1

    @rx.var
    def prev_poem(self) -> Optional[Poem]:
        """Returns the previous poem in the date-sorted list."""
        idx = self.current_poem_index
        if idx > 0 and idx < len(self._sorted_poems):
            return self._sorted_poems[idx - 1]
        return None

    @rx.var
    def next_poem(self) -> Optional[Poem]:
        """Returns the next poem in the date-sorted list."""
        idx = self.current_poem_index
        if 0 <= idx < len(self._sorted_poems) - 1:
            return self._sorted_poems[idx + 1]
        return None

    @rx.var
    def total_poem_count(self) -> int:
        """Returns the total number of poems."""
        return len(self._sorted_poems)

    @rx.event
    def go_to_poem(self):
        """Placeholder event for navigation. Navigation is now handled by hrefs."""
        pass

    @rx.var
    def poem_stanzas(self) -> list[str]:
        """Groups poem content lines into stanzas."""
        if not self.selected_poem or not self.selected_poem["content"]:
            return []
        stanzas = []
        current_stanza = []
        for line in self.selected_poem["content"]:
            if line.strip() == "":
                if current_stanza:
                    stanzas.append(
                        """
""".join(current_stanza)
                    )
                    current_stanza = []
            else:
                current_stanza.append(line)
        if current_stanza:
            stanzas.append(
                """
""".join(current_stanza)
            )
        return stanzas

    @rx.var
    def filtered_poems(self) -> list[Poem]:
        """Returns a list of poems filtered by search term and sorted."""
        poems_to_filter = [
            p
            for p in self.poems
            if not (self.preamble_poem and p["id"] == self.preamble_poem["id"])
        ]
        if self.search_term:
            search_lower = self.search_term.lower()
            poems_to_filter = [
                p
                for p in poems_to_filter
                if search_lower in p["title"].lower()
                or search_lower in p["excerpt"].lower()
            ]
        reverse = self.sort_by == "Recent"
        if "Date" in self.sort_by or self.sort_by == "Recent":
            return sorted(
                poems_to_filter, key=lambda p: p.get("date", ""), reverse=reverse
            )
        elif "Title" in self.sort_by:
            return sorted(poems_to_filter, key=lambda p: p["title"], reverse=False)
        return sorted(poems_to_filter, key=lambda p: p.get("date", ""), reverse=reverse)

    @rx.var
    def collection_stats(self) -> str:
        """Returns a string with collection statistics."""
        total = len(self.poems)
        filtered = len(self.filtered_poems)
        if self.search_term or self.sort_by != "Recent":
            return f"Showing {filtered} of {total} poems"
        return f"{total} poems in collection"

    @rx.event(background=True)
    async def fetch_poems(self):
        """
        Fetch poems from the Notion database in the background.
        """
        async with self:
            if not self.is_loading:
                self.is_loading = True
            self.error_message = ""
        try:
            notion_token = os.getenv("NOTION_API_KEY")
            if not notion_token:
                async with self:
                    self.error_message = "NOTION_API_KEY is not set. Please add it to your environment variables."
                    self.is_loading = False
                return
            notion = AsyncClient(auth=notion_token)
            db_query = await notion.databases.query(database_id=self.database_id)
            tasks = [
                self._process_page(notion, page) for page in db_query.get("results", [])
            ]
            processed_poems = await asyncio.gather(*tasks)
            processed_poems = [p for p in processed_poems if p]
            preamble = next(
                (p for p in processed_poems if p["title"].lower() == "lost"), None
            )
            async with self:
                self.poems = processed_poems
                if preamble:
                    self.preamble_poem = preamble
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Failed to fetch poems: {e}")
            async with self:
                self.error_message = f"Failed to fetch poems: {str(e)}"
                self.is_loading = False

    @rx.event(background=True)
    async def handle_idle(self):
        async with self:
            self.idle = True
        await asyncio.sleep(5)
        async with self:
            self.idle = False

    @rx.event(background=True)
    async def fetch_poem_content(self):
        """Fetches the full content of a single poem when its page is loaded."""
        poem_id = self.router.page.params.get("poem_id", "")
        if not poem_id:
            return
        async with self:
            self.is_poem_loading = True
            self.error_message = ""
            self.selected_poem = None
        try:
            async with self:
                poems_loaded = bool(self.poems)
            if not poems_loaded:
                yield PoetryState.fetch_poems
            poem_data = None
            async with self:
                if self.preamble_poem and self.preamble_poem["id"] == poem_id:
                    poem_data = self.preamble_poem.copy()
                else:
                    found_poem = next(
                        (p for p in self.poems if p["id"] == poem_id), None
                    )
                    if found_poem:
                        poem_data = found_poem.copy()
                self.selected_poem = poem_data
            if not poem_data:
                async with self:
                    self.error_message = "Poem not found."
                    self.is_poem_loading = False
                return
            notion_token = os.getenv("NOTION_API_KEY")
            if not notion_token:
                async with self:
                    self.error_message = "Notion API key not configured."
                    self.is_poem_loading = False
                return
            notion = AsyncClient(auth=notion_token)
            blocks_result = await notion.blocks.children.list(block_id=poem_id)
            content_lines = []
            for block in blocks_result.get("results", []):
                if block["type"] == "paragraph":
                    text_parts = block.get("paragraph", {}).get("rich_text", [])
                    line = "".join([t["plain_text"] for t in text_parts])
                    content_lines.append(line)
            async with self:
                if self.selected_poem:
                    poem_data = self.selected_poem.copy()
                    poem_data["content"] = content_lines
                    self.selected_poem = poem_data
                self.is_poem_loading = False
        except Exception as e:
            logging.exception(f"Failed to fetch poem content for ID {poem_id}: {e}")
            async with self:
                self.error_message = f"A problem occurred while loading the poem."
                self.is_poem_loading = False

    async def _process_page(self, notion: AsyncClient, page: dict) -> Optional[Poem]:
        """Helper to process a single Notion page into a Poem object."""
        try:
            page_id = page["id"]
            properties = page.get("properties", {})
            title_prop = properties.get("Title", {}).get("title", [])
            title = title_prop[0]["plain_text"] if title_prop else "Untitled"
            date_prop = properties.get("Date", {}).get("date", {})
            date = date_prop.get("start", "") if date_prop else ""
            image_prop = properties.get("Image", {}).get("files", [])
            image_url = (
                image_prop[0]["file"]["url"]
                if image_prop and image_prop[0].get("file")
                else None
            )
            blocks = await notion.blocks.children.list(block_id=page_id, page_size=5)
            excerpt_lines = []
            for block in blocks.get("results", []):
                if block["type"] == "paragraph":
                    text_parts = block.get("paragraph", {}).get("rich_text", [])
                    if text_parts:
                        excerpt_lines.append(text_parts[0]["plain_text"])
            excerpt = (
                " ".join(excerpt_lines[:3]) + "..." if excerpt_lines else "No content."
            )
            return {
                "id": page_id,
                "title": title,
                "date": date,
                "image_url": image_url,
                "excerpt": excerpt,
                "content": [],
            }
        except Exception as e:
            logging.exception(f"Failed to process page: {e}")
            return None