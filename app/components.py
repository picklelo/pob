import reflex as rx
from app.state import PoetryState, Poem


def app_footer() -> rx.Component:
    """A shared footer for all pages."""
    return rx.el.footer(
        rx.el.div(
            rx.el.p(
                "Thank you for staying.",
                class_name=rx.cond(
                    PoetryState.scrolled_to_bottom,
                    "text-center text-sm text-gray-400/80 mb-8 transition-opacity duration-1000 opacity-100 font-['Fraunces'] italic",
                    "text-center text-sm text-gray-400/80 mb-8 transition-opacity duration-1000 opacity-0 font-['Fraunces'] italic",
                ),
            ),
            rx.el.p(
                "© Nikhil Rao — The Privilege of Boredom",
                class_name="font-['Inter'] text-center text-xs text-gray-500/50 pb-12",
            ),
        ),
        class_name="w-full flex-shrink-0 mt-24",
    )


def filter_controls() -> rx.Component:
    """Controls for searching and sorting poems."""
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500/70",
            ),
            rx.el.input(
                placeholder="Search...",
                on_change=PoetryState.set_search_term,
                class_name="w-full pl-9 pr-4 py-2 bg-transparent border-b border-white/10 focus:ring-0 focus:border-[#B7926F] transition text-[#F3F1EE] placeholder-gray-500 font-['Inter']",
                default_value=PoetryState.search_term,
            ),
            class_name="relative flex-grow",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    PoetryState.sort_options,
                    lambda option: rx.el.option(
                        option, value=option, class_name="bg-gray-900 text-[#F3F1EE]"
                    ),
                ),
                value=PoetryState.sort_by,
                on_change=PoetryState.set_sort_by,
                class_name="w-full bg-transparent border-b border-white/10 px-4 py-2 appearance-none focus:ring-0 focus:border-[#B7926F] transition text-[#F3F1EE] font-['Inter']",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500/70 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex flex-col md:flex-row gap-6 mb-8",
    )


def preamble_card(poem: Poem) -> rx.Component:
    """A special card for the preamble poem, styled as an opening page."""
    return rx.el.a(
        rx.el.h2(
            poem["title"],
            class_name="text-4xl font-['Fraunces'] font-medium text-[#F3F1EE] transition-colors duration-300 hover:text-white/80",
            style={"textShadow": "0 2px 30px rgba(0, 0, 0, 0.2)"},
        ),
        href=f"/poem/{poem['id']}",
        class_name="w-full flex flex-col items-center text-center py-16 transition-all duration-400 ease-in-out preamble-fade-in mb-16",
    )


def poem_card(poem: Poem) -> rx.Component:
    """A component to display a single poem title in the list."""
    return rx.el.a(
        rx.el.div(
            rx.el.h3(
                poem["title"],
                class_name="text-2xl font-['Fraunces'] text-[#EAE6DF] group-hover:text-white transition-colors duration-300",
            ),
            rx.el.p(
                poem["date"], class_name="text-sm text-gray-600 font-['Inter'] mt-1"
            ),
            class_name="flex-1",
        ),
        rx.icon(
            "arrow-right",
            class_name="text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300",
        ),
        href=f"/poem/{poem['id']}",
        class_name="w-full flex items-center justify-between py-6 border-b border-white/5 transition-all duration-300 ease-in-out group poem-fade-in",
    )


def skeleton_card() -> rx.Component:
    """A skeleton loading card for the poem list."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-6 w-3/5 bg-gray-800 rounded-md"),
            rx.el.div(class_name="h-4 w-1/4 bg-gray-800 rounded-md mt-2"),
        ),
        class_name="w-full py-6 border-b border-white/5 animate-pulse",
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
                    class_name="w-full",
                ),
            ),
        ),
    )