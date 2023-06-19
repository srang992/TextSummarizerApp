import flet as ft
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from ionicons_python.extra_icons import chatgpt_icon
from custom_flet.components.custom_icon import CustomIcon


def main(page: ft.Page):
    page.fonts = {
        "Courgette": "fonts/Courgette-Regular.ttf",
        "Alkatra": "fonts/Alkatra-Regular.ttf"
    }
    page.theme = ft.Theme(
        primary_swatch=ft.colors.BLUE
    )
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    full_text_field = ft.Ref[ft.TextField]()
    token_field = ft.Ref[ft.TextField]()
    submit_button = ft.Ref[ft.ElevatedButton]()

    def on_submit_button(_):
        if not full_text_field.current.value and not token_field.current.value:
            page.snack_bar = ft.SnackBar(ft.Text("Enter Text and Token First!", font_family="Alkatra"), open=True)
            page.update()
            return
        elif not full_text_field.current.value:
            page.snack_bar = ft.SnackBar(ft.Text("Enter Text First!", font_family="Alkatra"), open=True)
            page.update()
            return
        elif not token_field.current.value:
            page.snack_bar = ft.SnackBar(ft.Text("Enter Token First!", font_family="Alkatra"), open=True)
            page.update()
            return
        elif not token_field.current.value.startswith("sk-"):
            page.snack_bar = ft.SnackBar(ft.Text("Invalid Token!", font_family="Alkatra"), open=True)
            page.update()
            return
        else:
            page.splash = ft.ProgressBar()
            submit_button.current.disabled = True
            page.update()
            llm = OpenAI(temperature=0, openai_api_key=token_field.current.value)
            text_splitter = CharacterTextSplitter()
            texts = text_splitter.split_text(full_text_field.current.value)
            docs = [Document(page_content=t) for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            response = chain.run(docs)
            full_text_field.current.value = f"Summarized Text is:\n\n{response}"
            token_field.current.value = None
            page.splash = None
            submit_button.current.disabled = False
            page.update()

    page.add(
        ft.Row(
            [
                CustomIcon(
                    icon=chatgpt_icon,
                    size=36,
                ),
                ft.Text(
                    "Text Summarizer App",
                    size=32,
                    font_family="Courgette",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(color=ft.colors.TRANSPARENT, height=5),
        ft.TextField(
            min_lines=14,
            max_lines=14,
            border_color=ft.colors.GREY_400,
            focused_border_color=ft.colors.BLUE,
            hint_text="Enter Text",
            hint_style=ft.TextStyle(
                font_family="Courgette"
            ),
            multiline=True,
            text_style=ft.TextStyle(
                font_family="Alkatra"
            ),
            width=600,
            ref=full_text_field,
        ),
        ft.TextField(
            border_color=ft.colors.GREY_400,
            focused_border_color=ft.colors.BLUE,
            hint_text="Enter OpenAI Secret Key",
            hint_style=ft.TextStyle(
                font_family="Courgette"
            ),
            text_style=ft.TextStyle(
                font_family="Alkatra"
            ),
            password=True,
            can_reveal_password=True,
            width=600,
            ref=token_field
        ),
        ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.CALCULATE),
                    ft.Text("Submit", size=16, font_family="Courgette"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=576,
            ),
            style=ft.ButtonStyle(
                padding=12
            ),
            on_click=on_submit_button,
            ref=submit_button,
        )
    )


ft.app(
    target=main,
    view=ft.WEB_BROWSER,
    port=8550,
    assets_dir="assets",
)
