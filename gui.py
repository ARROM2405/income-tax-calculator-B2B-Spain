import flet as ft
from flet_core import FontWeight, TextThemeStyle, TextAlign

ft.UserControl


def main(page: ft.Page):
    page.title = "Spanish tax calculator"
    label = ft.Text(
        value="Spanish income tax calculator. Creator is not tax expert, "
        "calculator is mostly created to perform approximate calculations.",
        weight=FontWeight.BOLD,
        style=TextThemeStyle.BODY_LARGE,
        text_align=TextAlign.CENTER,
    )

    monthly_salary_input = ft.TextField(label="Monthly receipt amount.")

    page.add(label, monthly_salary_input)

    page.update()


ft.app(target=main)
