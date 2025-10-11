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
    reading_mode: bool = False
    idle: bool = False

    @rx.var
    def _sorted_poems(self) -> list[Poem]:
        """Returns poems sorted by date, which is the base for navigation."""
        return sorted(self.poems, key=lambda p: p.get("date", ""), reverse=True)

    @rx.var
    def current_poem_index(self) -> int:
        """Returns the index of the currently selected poem in the date-sorted list."""
        if not self.selected_poem:
            return -1
        try:
            return self._sorted_poems.index(self.selected_poem)
        except ValueError as e:
            logging.exception(f"Error finding poem index: {e}")
            return -1

    @rx.var
    def prev_poem(self) -> Optional[Poem]:
        """Returns the previous poem in the date-sorted list."""
        if self.current_poem_index > 0:
            return self._sorted_poems[self.current_poem_index - 1]
        return None

    @rx.var
    def next_poem(self) -> Optional[Poem]:
        """Returns the next poem in the date-sorted list."""
        if 0 <= self.current_poem_index < len(self._sorted_poems) - 1:
            return self._sorted_poems[self.current_poem_index + 1]
        return None

    @rx.var
    def total_poem_count(self) -> int:
        """Returns the total number of poems."""
        return len(self._sorted_poems)

    @rx.event
    def share_poem(self) -> rx.event.EventSpec:
        """Exports the current poem's content to a text file for sharing."""
        if self.selected_poem:
            title = self.selected_poem["title"].replace(" ", "_")
            content = """
""".join(self.selected_poem["content"])
            return rx.download(data=content, filename=f"{title}.txt")
        return rx.noop()

    @rx.var
    def is_favorite(self) -> bool:
        """Check if the selected poem is in the favorites list."""
        if self.selected_poem:
            return self.selected_poem["id"] in self.favorite_ids
        return False

    @rx.event
    def toggle_favorite(self, poem_id: str):
        """Toggle the favorite status of a poem."""
        if poem_id in self.favorite_ids:
            self.favorite_ids.remove(poem_id)
        else:
            self.favorite_ids.append(poem_id)
        return self._save_favorites()

    @rx.event
    def load_favorites(self):
        """Load favorite poem IDs from local storage."""
        return rx.call_script(
            "localStorage.getItem('favorite_ids')", callback=self._on_favorites_loaded
        )

    def _on_favorites_loaded(self, stored_ids: str):
        if stored_ids:
            self.favorite_ids = json.loads(stored_ids)

    def _save_favorites(self):
        """Save favorite IDs to local storage."""
        return rx.call_script(
            f"localStorage.setItem('favorite_ids', '{json.dumps(self.favorite_ids)}')"
        )

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

    @rx.event
    async def toggle_reading_mode(self):
        self.reading_mode = not self.reading_mode

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
        async with self:
            self.is_poem_loading = True
            self.error_message = ""
        try:
            if not self.poems:
                await self.fetch_poems()
            async with self:
                if self.preamble_poem and self.preamble_poem["id"] == poem_id:
                    poem_data = self.preamble_poem
                else:
                    poem_data = next(
                        (p for p in self.poems if p["id"] == poem_id), None
                    )
            if not poem_data:
                async with self:
                    self.error_message = "Poem not found."
                    self.is_poem_loading = False
                return
            notion_token = os.getenv("NOTION_API_KEY")
            notion = AsyncClient(auth=notion_token)
            blocks_result = await notion.blocks.children.list(block_id=poem_id)
            content_lines = []
            for block in blocks_result.get("results", []):
                if block["type"] == "paragraph":
                    text_parts = block.get("paragraph", {}).get("rich_text", [])
                    line = "".join((t["plain_text"] for t in text_parts))
                    content_lines.append(line)
            async with self:
                poem_data["content"] = content_lines
                self.selected_poem = poem_data
                self.is_poem_loading = False
        except Exception as e:
            logging.exception(f"Failed to fetch poem content: {e}")
            async with self:
                self.error_message = f"Failed to fetch poem: {str(e)}"
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