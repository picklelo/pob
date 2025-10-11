import reflex as rx
from app.state import PoetryState, Poem


def filter_controls() -> rx.Component:
    """Controls for searching and sorting poems."""
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-500",
            ),
            rx.el.input(
                placeholder="Search by title or feeling…",
                on_change=PoetryState.set_search_term,
                class_name="w-full pl-10 pr-4 py-2.5 rounded-lg border border-white/10 bg-black/20 focus:ring-2 focus:ring-[#B7926F] focus:border-transparent transition text-[#F3F1EE] placeholder-gray-500 font-['Inter']",
                default_value=PoetryState.search_term,
            ),
            class_name="relative flex-grow",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    PoetryState.sort_options,
                    lambda option: rx.el.option(
                        option, value=option, class_name="bg-gray-800 text-[#F3F1EE]"
                    ),
                ),
                value=PoetryState.sort_by,
                on_change=PoetryState.set_sort_by,
                class_name="w-full rounded-lg border border-white/10 bg-black/20 px-4 py-2.5 appearance-none focus:ring-2 focus:ring-[#B7926F] focus:border-transparent transition text-[#F3F1EE] font-['Inter']",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex flex-col md:flex-row gap-4 mb-8",
    )


def poem_card(poem: Poem) -> rx.Component:
    """A card component to display a single poem in a vertical list."""
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    poem["title"],
                    class_name="text-lg font-['Fraunces'] text-[#F3F1EE] group-hover:text-[#B7926F] transition-colors duration-300",
                    style={"textShadow": "0 2px 10px rgba(183, 146, 111, 0.3)"},
                ),
                rx.el.p(
                    poem["date"],
                    class_name="text-sm font-light text-gray-500 font-['Inter']",
                ),
            ),
            rx.el.p(
                poem["excerpt"],
                class_name="text-sm text-gray-400 mt-3 font-['Inter'] leading-relaxed",
            ),
            class_name="flex-1",
        ),
        rx.icon(
            "chevron-right",
            class_name="text-gray-600 group-hover:text-[#B7926F] transition-transform group-hover:translate-x-1 duration-300",
        ),
        href=f"/poem/{poem['id']}",
        class_name="w-full flex items-center justify-between p-6 bg-black/10 border border-white/5 rounded-2xl transition-all duration-300 ease-in-out group hover:border-[#B7926F]/30 hover:bg-black/20 poem-fade-in",
    )


def skeleton_card() -> rx.Component:
    """A skeleton loading card for the vertical list view."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-5 w-1/2 bg-gray-800 rounded-lg"),
            rx.el.div(class_name="h-4 w-1/4 bg-gray-800 rounded-lg mt-2"),
            class_name="flex-1",
        ),
        rx.el.div(class_name="h-4 w-3/4 bg-gray-800 rounded-lg mt-3"),
        class_name="w-full p-6 bg-black/10 border border-white/5 rounded-2xl animate-pulse",
    )


def poetry_grid() -> rx.Component:
    """The main grid to display poems."""
    return rx.cond(
        PoetryState.is_loading,
        rx.el.div(
            rx.foreach([1, 2, 3], lambda _: skeleton_card()),
            class_name="w-full space-y-4",
        ),
        rx.cond(
            PoetryState.error_message != "",
            rx.el.div(
                rx.icon("flag_triangle_right", size=48, class_name="text-red-400"),
                rx.el.h2(
                    "An Error Occurred",
                    class_name="text-2xl font-bold mt-4 text-gray-200",
                ),
                rx.el.p(PoetryState.error_message, class_name="text-gray-400 mt-2"),
                class_name="flex flex-col items-center justify-center bg-red-900/20 border border-red-500/30 p-12 rounded-2xl",
            ),
            rx.cond(
                PoetryState.filtered_poems.length() == 0,
                rx.el.div(
                    rx.icon("search-slash", size=48, class_name="text-gray-500"),
                    rx.el.h2(
                        "No Poems Found",
                        class_name="text-2xl font-bold mt-4 text-gray-300",
                    ),
                    rx.el.p(
                        "Try adjusting your search or filter.",
                        class_name="text-gray-500 mt-2",
                    ),
                    class_name="flex flex-col items-center justify-center text-center bg-black/20 p-12 rounded-2xl",
                ),
                rx.el.div(
                    rx.foreach(PoetryState.filtered_poems, poem_card),
                    class_name="w-full space-y-4",
                ),
            ),
        ),
    )