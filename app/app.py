import reflex as rx
from app.state import PoetryState
from app.components import poetry_grid, filter_controls, preamble_card, app_footer
import asyncio


def poem_detail_page() -> rx.Component:
    """A page to display the full details of a single poem."""
    return rx.el.div(
        rx.el.div(class_name="vignette-overlay pointer-events-none"),
        rx.el.main(
            rx.el.p(
                "be still.",
                class_name=rx.cond(
                    PoetryState.idle,
                    "fixed inset-0 flex items-center justify-center text-2xl font-['Fraunces'] text-white/30 z-50 transition-opacity duration-1000 opacity-100",
                    "fixed inset-0 flex items-center justify-center text-2xl font-['Fraunces'] text-white/30 z-50 transition-opacity duration-1000 opacity-0 pointer-events-none",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.a(
                            rx.icon("arrow-left", size=16, class_name="mr-2"),
                            "Back to Collection",
                            href="/",
                            class_name="flex items-center text-[#B7926F] font-['Inter'] transition-opacity hover:opacity-80",
                        ),
                        rx.el.button(
                            rx.icon("book-open", size=16),
                            on_click=PoetryState.toggle_reading_mode,
                            class_name="p-2 rounded-md hover:bg-white/10 transition-colors",
                            color_scheme="none",
                        ),
                        class_name="flex items-center justify-between w-full max-w-3xl px-8 md:px-12",
                    ),
                    class_name=rx.cond(
                        PoetryState.reading_mode,
                        "opacity-0 transition-opacity fixed top-8 left-1/2 -translate-x-1/2 z-10 w-full",
                        "opacity-100 transition-opacity w-full",
                    ),
                ),
                rx.cond(
                    PoetryState.is_poem_loading,
                    rx.el.div(
                        rx.el.div(
                            class_name="h-8 w-3/5 bg-gray-800 rounded-lg animate-pulse mb-4"
                        ),
                        rx.el.div(
                            class_name="h-4 w-1/4 bg-gray-800 rounded-lg animate-pulse mb-12"
                        ),
                        rx.el.div(
                            class_name="h-5 w-full bg-gray-800 rounded-lg animate-pulse mb-3"
                        ),
                        rx.el.div(
                            class_name="h-5 w-5/6 bg-gray-800 rounded-lg animate-pulse mb-3"
                        ),
                        rx.el.div(
                            class_name="h-5 w-3/4 bg-gray-800 rounded-lg animate-pulse mb-8"
                        ),
                        rx.el.div(
                            class_name="h-5 w-full bg-gray-800 rounded-lg animate-pulse mb-3"
                        ),
                        rx.el.div(
                            class_name="h-5 w-2/3 bg-gray-800 rounded-lg animate-pulse mb-3"
                        ),
                        class_name="w-full poem-fade-in max-w-3xl p-8 md:p-12",
                    ),
                    rx.cond(
                        PoetryState.error_message != "",
                        rx.el.div(
                            rx.icon(
                                "flag_triangle_right",
                                size=48,
                                class_name="text-red-400",
                            ),
                            rx.el.h2(
                                "An Error Occurred",
                                class_name="text-2xl font-['Fraunces'] mt-4 text-[#F3F1EE]",
                            ),
                            rx.el.p(
                                PoetryState.error_message,
                                class_name="text-gray-400 mt-2 font-['Inter']",
                            ),
                            class_name="flex flex-col items-center justify-center bg-red-900/20 border border-red-500/30 p-12 rounded-2xl",
                        ),
                        rx.el.div(
                            rx.el.div(class_name="h-12"),
                            rx.cond(
                                PoetryState.selected_poem["image_url"],
                                rx.image(
                                    src=PoetryState.selected_poem["image_url"],
                                    class_name="w-full h-64 object-cover rounded-xl mb-8 shadow-lg shadow-black/20",
                                ),
                            ),
                            rx.el.h1(
                                PoetryState.selected_poem["title"],
                                class_name="text-4xl md:text-5xl font-['Fraunces'] text-[#F3F1EE] mb-2",
                                style={
                                    "textShadow": "0 2px 20px rgba(183, 146, 111, 0.3)"
                                },
                            ),
                            rx.el.p(
                                PoetryState.selected_poem["date"],
                                class_name=rx.cond(
                                    PoetryState.reading_mode,
                                    "opacity-0 transition-opacity text-md text-gray-500 mb-12 font-['Inter']",
                                    "opacity-100 transition-opacity text-md text-gray-500 mb-12 font-['Inter']",
                                ),
                            ),
                            rx.el.div(
                                rx.foreach(
                                    PoetryState.selected_poem["content"],
                                    lambda line: rx.el.p(
                                        line,
                                        class_name="text-xl text-[#F3F1EE]/80 font-['Inter']",
                                        style={"lineHeight": 1.8},
                                    ),
                                ),
                                class_name="space-y-4 max-w-none poem-fade-in",
                            ),
                        ),
                    ),
                ),
                class_name="p-8 md:p-12 w-full max-w-3xl transition-all duration-500",
                id="poem-content",
            ),
            rx.el.div(
                rx.cond(
                    PoetryState.prev_poem,
                    rx.el.button(
                        rx.icon("arrow-left", size=16, class_name="mr-2"),
                        rx.el.span("Previous: "),
                        rx.el.span(
                            PoetryState.prev_poem["title"],
                            class_name="font-['Fraunces']",
                        ),
                        on_click=lambda: PoetryState.go_to_poem(
                            PoetryState.prev_poem["id"]
                        ),
                        class_name="flex items-center text-gray-400 hover:text-[#B7926F] transition-colors duration-300",
                    ),
                    rx.el.div(),
                ),
                rx.el.p(
                    f"{PoetryState.current_poem_index + 1} of {PoetryState.total_poem_count}",
                    class_name="text-gray-500 font-['Inter'] text-sm",
                ),
                rx.cond(
                    PoetryState.next_poem,
                    rx.el.button(
                        rx.el.span(
                            PoetryState.next_poem["title"],
                            class_name="font-['Fraunces']",
                        ),
                        rx.el.span(" :Next"),
                        rx.icon("arrow-right", size=16, class_name="ml-2"),
                        on_click=lambda: PoetryState.go_to_poem(
                            PoetryState.next_poem["id"]
                        ),
                        class_name="flex items-center text-gray-400 hover:text-[#B7926F] transition-colors duration-300",
                    ),
                    rx.el.div(),
                ),
                class_name=rx.cond(
                    PoetryState.reading_mode,
                    "opacity-0 transition-opacity flex justify-between items-center w-full max-w-3xl mt-8 px-4",
                    "opacity-100 transition-opacity flex justify-between items-center w-full max-w-3xl mt-8 px-4",
                ),
            ),
            app_footer(),
            class_name=rx.cond(
                PoetryState.reading_mode,
                "w-full min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 md:p-8",
                "w-full min-h-screen flex flex-col items-center justify-start pt-24 p-4 sm:p-6 md:p-8",
            ),
        ),
        on_mount=[
            PoetryState.fetch_poem_content,
            rx.call_script(
                "(function() { let timeout; function resetTimer() { clearTimeout(timeout); timeout = setTimeout(() => { E_PoetryState.handle_idle(); }, 30000); } document.onmousemove = resetTimer; document.onkeypress = resetTimer; resetTimer(); })()"
            ),
        ],
        class_name="min-h-screen text-[#F3F1EE] poem-detail-crossfade poetic-gradient",
    )


def index() -> rx.Component:
    """The main page of the app."""
    return rx.el.div(
        rx.el.div(class_name="vignette-overlay pointer-events-none"),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "The Privilege of Boredom",
                        class_name="text-4xl md:text-5xl font-['Fraunces'] text-[#F3F1EE] mt-4",
                        style={"textShadow": "0 2px 20px rgba(183, 146, 111, 0.3)"},
                    ),
                    rx.el.h2(
                        "poems from before and after the break.",
                        class_name="text-lg text-gray-400 mt-2 font-['Inter']",
                    ),
                    rx.el.p(
                        "Attention is costly. Boredom is a luxury.",
                        class_name="text-gray-500 mt-8 font-['Inter']",
                    ),
                    class_name="text-center mb-12 poem-fade-in",
                ),
                rx.cond(
                    PoetryState.preamble_poem, preamble_card(PoetryState.preamble_poem)
                ),
                rx.el.div(
                    filter_controls(), poetry_grid(), class_name="space-y-6 mt-12"
                ),
                class_name="max-w-3xl mx-auto w-full",
            ),
            app_footer(),
            on_mount=PoetryState.fetch_poems,
            class_name="min-h-screen text-[#F3F1EE] flex flex-col items-center p-4 sm:p-6 md:py-12",
        ),
        class_name="poetic-gradient",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,700&family=Inter:wght@300;400;500&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=["/style.css"],
)
app.add_page(index)
app.add_page(poem_detail_page, route="/poem/[poem_id]")