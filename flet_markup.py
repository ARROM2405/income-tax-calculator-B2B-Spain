import flet as ft
import flet_core
from flet_core import TextAlign, TextThemeStyle, FontWeight

from custom_classes import Block, TextFieldWithErrorField
from enums import Currency
from utils import (
    activate_on_dropdown_change,
    validate_text_field_numeric,
    activate_on_checkbox_change,
)


def main(page: ft.Page):
    page.title = "B2B in Spain tax calculator"

    # input_block_controls = []
    # output_block = Block()
    errors_block = Block()

    main_label = ft.Text(
        value="Spanish income tax calculator. Creator is not tax expert, "
        "calculator is mostly created to perform approximate calculations.",
        weight=FontWeight.BOLD,
        style=TextThemeStyle.BODY_LARGE,
        text_align=TextAlign.CENTER,
    )

    # errors

    # error = ft.Text(
    #     value="",
    #     weight=FontWeight.BOLD,
    #     visible=False,
    #     color=flet_core.colors.ERROR,
    #     text_align=flet_core.TextAlign.CENTER,
    # )
    # errors_block.add(error)

    # salary block

    currency_rate = TextFieldWithErrorField.get_field_with_added_error(
        label="Salary currency / EUR rate",
        disabled=True,
        expand=True,
        hint_text="Example: 1.52",
        col=2,
        validation_numeric_type=float,
        page=page,
    )
    currency_dropdown = ft.Dropdown(
        label="Salary currency",
        options=[
            ft.dropdown.Option(Currency.EUR.value),
            ft.dropdown.Option(Currency.OTHER.value),
        ],
        on_change=activate_on_dropdown_change(currency_rate, page),
        col=2,
    )

    responsive_row_salary_currency = ft.ResponsiveRow(
        controls=[
            currency_dropdown,
            currency_rate,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        columns=4,
    )

    receipts_per_year = ft.Dropdown(
        label="Receipts annually",
        options=[ft.dropdown.Option(_) for _ in range(1, 21)],
        col=2,
    )

    monthly_receipt = ft.TextField(
        label="Monthly receipt in chosen currency",
        on_change=validate_text_field_numeric(error, page, float),
        hint_text="Example: 1.52",
        expand=True,
        col=2,
    )

    responsive_row_monthly_receipt = ft.ResponsiveRow(
        controls=[receipts_per_year, monthly_receipt], columns=4
    )

    # input_block_controls.extend(
    #     [
    #         responsive_row_salary_currency,
    #         responsive_row_monthly_receipt,
    #     ]
    # )

    # input_block.add(
    #     currency_dropdown,
    #     currency_rate,
    #     monthly_receipt,
    #     receipts_per_year,
    # )
    # input_block.to_row(
    #     row_controls_count=2,
    #     # wrap=True,
    #     expand=True,
    #     alignment=ft.MainAxisAlignment.CENTER,
    # )

    # tax-free allowance block

    kids_count_text_field = ft.TextField(
        label="Kids count",
        hint_text="if more than 4 kids, count only those 3 years younger",
        disabled=True,
        col=2,
        on_change=validate_text_field_numeric(error, page, int),
    )
    kids_tax_free_allowance_checkbox = ft.Checkbox(
        label="Kids under 25 living with you",
        on_change=activate_on_checkbox_change(
            text_field=kids_count_text_field,
            page=page,
        ),
        col=2,
    )

    kids_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[kids_tax_free_allowance_checkbox, kids_count_text_field],
        columns=4,
    )

    over_65_tax_free_allowance_count_text_field = ft.TextField(
        label="Elder over 65 count",
        disabled=True,
        col=2,
        on_change=validate_text_field_numeric(error, page, int),
    )
    over_65_checkbox = ft.Checkbox(
        label="Elder over 65 living with you",
        on_change=activate_on_checkbox_change(
            text_field=over_65_tax_free_allowance_count_text_field,
            page=page,
        ),
        col=2,
    )

    over_65_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[over_65_checkbox, over_65_tax_free_allowance_count_text_field],
        columns=4,
    )
    over_75_tax_free_allowance_count_text_field = ft.TextField(
        label="Elder over 75 count",
        disabled=True,
        col=2,
        on_change=validate_text_field_numeric(error, page, int),
    )
    over_75_checkbox = ft.Checkbox(
        label="Elder over 65 living with you",
        on_change=activate_on_checkbox_change(
            text_field=over_75_tax_free_allowance_count_text_field,
            page=page,
        ),
        col=2,
    )

    over_75_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[over_75_checkbox, over_75_tax_free_allowance_count_text_field],
        columns=4,
    )

    page.add(
        main_label,
        responsive_row_salary_currency,
        responsive_row_monthly_receipt,
        *errors_block.controls,
        kids_tax_free_allowance_row,
        over_65_tax_free_allowance_row,
        over_75_tax_free_allowance_row,
    )
    page.update()


ft.app(target=main)
