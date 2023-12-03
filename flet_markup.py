import flet as ft
from flet_core import TextAlign, TextThemeStyle, FontWeight

from custom_classes import (
    TextFieldWithErrorField,
    ErrorsContainer,
    TextFieldsContainer,
    EnhancedElevatedButton,
)
from enums import Currency
from utils import (
    activate_on_dropdown_change,
    activate_on_checkbox_change,
    some_test_on_click,
    add_page_controls,
)


def main(page: ft.Page):
    page.title = "B2B in Spain tax calculator"

    main_label = ft.Text(
        value="Spanish income tax calculator. Creator is not tax expert, "
        "calculator is mostly created to perform approximate calculations.",
        weight=FontWeight.BOLD,
        style=TextThemeStyle.BODY_LARGE,
        text_align=TextAlign.CENTER,
    )

    errors_container = ErrorsContainer()
    text_fields_container = TextFieldsContainer()

    submit_button = EnhancedElevatedButton(
        text="Submit",
        disabled=True,
        depend_on_error_fields=errors_container,
        depend_on_text_fields=text_fields_container,
        on_click=some_test_on_click,
    )

    currency_rate = TextFieldWithErrorField.get_field_with_added_error(
        label="Salary currency / EUR rate",
        disabled=True,
        expand=True,
        hint_text="Example: 1.52",
        col=2,
        validation_numeric_type=float,
        page=page,
        submit_button=submit_button,
        errors_container=errors_container,
        text_fields_container=text_fields_container,
    )
    currency_dropdown = ft.Dropdown(
        label="Salary currency",
        options=[
            ft.dropdown.Option(Currency.EUR.value),
            ft.dropdown.Option(Currency.OTHER.value),
        ],
        value=Currency.EUR.value,
        on_change=activate_on_dropdown_change(
            text_with_error_field=currency_rate,
            submit_button=submit_button,
            page=page,
        ),
        col=2,
    )

    responsive_row_salary_currency = ft.ResponsiveRow(
        controls=[
            currency_dropdown,
            currency_rate.text_field,
            currency_rate.error,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        columns=4,
    )

    receipts_per_year = ft.Dropdown(
        label="Receipts annually",
        options=[ft.dropdown.Option(_) for _ in range(1, 21)],
        col=2,
        value="1",
    )

    monthly_receipt = TextFieldWithErrorField.get_field_with_added_error(
        label="Monthly receipt in chosen currency",
        hint_text="Example: 1.52",
        expand=True,
        validation_numeric_type=float,
        page=page,
        col=2,
        submit_button=submit_button,
        errors_container=errors_container,
        text_fields_container=text_fields_container,
    )

    responsive_row_monthly_receipt = ft.ResponsiveRow(
        controls=[
            receipts_per_year,
            monthly_receipt.text_field,
            monthly_receipt.error,
        ],
        columns=4,
    )

    kids_count_text_field = TextFieldWithErrorField.get_field_with_added_error(
        label="Kids count",
        hint_text="if more than 4 kids, count only those 3 years younger",
        disabled=True,
        col=2,
        validation_numeric_type=int,
        page=page,
        submit_button=submit_button,
        errors_container=errors_container,
        text_fields_container=text_fields_container,
    )
    kids_tax_free_allowance_checkbox = ft.Checkbox(
        label="Kids under 25 living with you",
        on_change=activate_on_checkbox_change(
            text_field_with_error=kids_count_text_field,
            page=page,
            submit_button=submit_button,
        ),
        col=2,
    )

    kids_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[
            kids_tax_free_allowance_checkbox,
            kids_count_text_field.text_field,
            kids_count_text_field.error,
        ],
        columns=4,
    )

    over_65_tax_free_allowance_count_text_field = (
        TextFieldWithErrorField.get_field_with_added_error(
            label="Elder over 65 count",
            disabled=True,
            col=2,
            validation_numeric_type=int,
            page=page,
            submit_button=submit_button,
            errors_container=errors_container,
            text_fields_container=text_fields_container,
        )
    )
    over_65_checkbox = ft.Checkbox(
        label="Elder over 65 living with you",
        on_change=activate_on_checkbox_change(
            text_field_with_error=over_65_tax_free_allowance_count_text_field,
            page=page,
            submit_button=submit_button,
        ),
        col=2,
    )

    over_65_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[
            over_65_checkbox,
            over_65_tax_free_allowance_count_text_field.text_field,
            over_65_tax_free_allowance_count_text_field.error,
        ],
        columns=4,
    )
    over_75_tax_free_allowance_count_text_field = (
        TextFieldWithErrorField.get_field_with_added_error(
            label="Elder over 75 count",
            disabled=True,
            col=2,
            validation_numeric_type=int,
            page=page,
            submit_button=submit_button,
            errors_container=errors_container,
            text_fields_container=text_fields_container,
        )
    )
    over_75_checkbox = ft.Checkbox(
        label="Elder over 65 living with you",
        on_change=activate_on_checkbox_change(
            text_field_with_error=over_75_tax_free_allowance_count_text_field,
            page=page,
            submit_button=submit_button,
        ),
        col=2,
    )

    over_75_tax_free_allowance_row = ft.ResponsiveRow(
        controls=[
            over_75_checkbox,
            over_75_tax_free_allowance_count_text_field.text_field,
            over_75_tax_free_allowance_count_text_field.error,
        ],
        columns=4,
    )

    add_page_controls(
        page=page,
        main_label=main_label,
        responsive_row_salary_currency=responsive_row_salary_currency,
        responsive_row_monthly_receipt=responsive_row_monthly_receipt,
        kids_tax_free_allowance_row=kids_tax_free_allowance_row,
        over_65_tax_free_allowance_row=over_65_tax_free_allowance_row,
        over_75_tax_free_allowance_row=over_75_tax_free_allowance_row,
        submit_button=submit_button,
    )
    page.update()
