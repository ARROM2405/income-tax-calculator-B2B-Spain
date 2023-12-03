import typing
from typing import Callable
import flet as ft

from enums import Currency, Month
from input_fields_registry import input_fields_registry

if typing.TYPE_CHECKING:
    from custom_classes import (
        EnhancedElevatedButton,
        TextFieldWithErrorField,
    )


def if_negative_convert_to_zero(value: int | float) -> int | float:
    if value < 0:
        return 0
    return value


def activate_on_dropdown_change(
    text_with_error_field: "TextFieldWithErrorField",
    submit_button: "EnhancedElevatedButton",
    page: ft.Page,
) -> Callable:
    def on_change(e):
        if e.data == Currency.OTHER.value:
            text_with_error_field.text_field.disabled = False
        elif e.data == Currency.EUR.value:
            text_with_error_field.text_field.disabled = True
            text_with_error_field.text_field.value = None
            text_with_error_field.error.visible = False
        else:
            raise NotImplementedError
        submit_button.disability_update()
        page.update()

    return on_change


def validate_text_field_numeric(
    event,
    output_error_field: ft.Text,
    numeric_type: type(int) | type(float),
):
    try:
        if event.data:
            numeric_type(event.data)
    except ValueError:
        if numeric_type == int:
            numeric_type_message = "integer"
        elif numeric_type == float:
            numeric_type_message = "decimal"
        else:
            raise NotImplementedError
        output_error_field.visible = True
        output_error_field.value = (
            f"Not valid input value to the field: {event.control.label}. "
            f"Should be {numeric_type_message}."
        )
    else:
        if output_error_field.visible:
            output_error_field.visible = False


# TODO: use as  the validation function factory instead of validate_text_field_numeric
def validate_text_field(
    output_error_field: ft.Text,
    submit_button: "EnhancedElevatedButton",
    page: ft.Page,
    numeric_type: type(int) | type(float),
) -> Callable:
    def on_change(e):
        validate_text_field_numeric(
            e,
            output_error_field,
            numeric_type,
        )

        submit_button.disability_update()

        page.update()

    return on_change


def activate_on_checkbox_change(
    text_field_with_error: "TextFieldWithErrorField",
    page: ft.Page,
    submit_button: "EnhancedElevatedButton",
):
    def on_change(e):
        if text_field_with_error.text_field.disabled:
            text_field_with_error.text_field.disabled = False

        else:
            text_field_with_error.text_field.disabled = True
            text_field_with_error.text_field.value = None
            text_field_with_error.error.visible = False
        submit_button.disability_update()
        page.update()

    return on_change


def add_page_controls(*, page: ft.Page, **kwargs):
    input_fields_registry["page"] = page
    for k, v in kwargs.items():
        input_fields_registry[k] = v
        page.add(v)


def collect_tax_calculation_params() -> dict:
    params_dict = dict()
    annual_receipts = int(
        input_fields_registry["responsive_row_monthly_receipt"].controls[0].value
    )
    params_dict["annual_receipts"] = annual_receipts
    monthly_receipt = float(
        input_fields_registry["responsive_row_monthly_receipt"].controls[1].value
    )
    currency_dropdown_value = (
        input_fields_registry["responsive_row_salary_currency"].controls[0].value
    )
    if currency_dropdown_value == "other currency":
        currency_rate = float(
            input_fields_registry["responsive_row_salary_currency"].controls[1].value
        )
        params_dict["salary_other_currency"] = monthly_receipt
        params_dict["rate"] = currency_rate
    else:
        params_dict["salary_eur"] = monthly_receipt
    for registered_input, param_name in (
        ("kids_tax_free_allowance_row", "children_count"),
        ("over_65_tax_free_allowance_row", "over_65_count"),
        ("over_75_tax_free_allowance_row", "over_75_count"),
    ):
        checkbox_value = input_fields_registry[registered_input].controls[0].value
        if checkbox_value:
            params_dict[param_name] = int(
                input_fields_registry[registered_input].controls[1].value
            )
    return params_dict


def add_output_for_page(output_data: dict, page: ft.Page):
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(value="Month")),
            ft.DataColumn(ft.Text(value="Salary brutto, EUR"), numeric=True),
            ft.DataColumn(ft.Text(value="Income tax, EUR"), numeric=True),
            ft.DataColumn(ft.Text(value="Social deductions, EUR"), numeric=True),
            ft.DataColumn(ft.Text(value="Salary netto, EUR"), numeric=True),
        ]
    )

    for month in Month:
        try:
            data_for_month = output_data[month]
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(month.value))),
                        ft.DataCell(
                            ft.Text(value=f"{data_for_month['receipt_brutto']}")
                        ),
                        ft.DataCell(
                            ft.Text(value=f"{data_for_month['income_tax_amount']}")
                        ),
                        ft.DataCell(
                            ft.Text(
                                value=f"{data_for_month['social_security_deductions']}"
                            )
                        ),
                        ft.DataCell(
                            ft.Text(value=f"{data_for_month['receipt_netto']}")
                        ),
                    ]
                )
            )

        except KeyError:
            break
    list_view = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )
    list_view.controls.append(data_table)

    if any([isinstance(_, ft.ListView) for _ in page.controls]):
        for _ in page.controls:
            if isinstance(_, ft.ListView):
                page.controls[page.controls.index(_)] = list_view
    else:
        page.add(list_view)
    page.update()


def some_test_on_click(e):
    from tax_calculation import perform_calculations

    params = collect_tax_calculation_params()
    receipts_per_month_with_tax_deductions = perform_calculations(**params)
    add_output_for_page(
        output_data=receipts_per_month_with_tax_deductions,
        page=input_fields_registry["page"],
    )
