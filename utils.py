from typing import Callable
import flet as ft

from enums import Currency


def if_negative_convert_to_zero(value: int | float) -> int | float:
    if value < 0:
        return 0
    return value


def activate_on_dropdown_change(field: ft.Control, page: ft.Page) -> Callable:
    def on_change(e):
        if e.data == Currency.OTHER.value:
            field.disabled = False
        elif e.data == Currency.EUR.value:
            field.disabled = True
        else:
            raise NotImplementedError
        page.update()

    return on_change


def validate_text_field_numeric(
    output_error_field: ft.Text, page: ft.Page, numeric_type: type(int) | type(float)
) -> Callable:
    def on_change(e):
        try:
            if e.data:
                numeric_type(e.data)
        except ValueError:
            if numeric_type == int:
                numeric_type_message = "integer"
            elif numeric_type == float:
                numeric_type_message = "decimal"
            else:
                raise NotImplementedError
            output_error_field.visible = True
            output_error_field.value = (
                f"Not valid input value to the field: {e.control.label}. "
                f"Should be {numeric_type_message}."
            )
            page.update()
        else:
            if output_error_field.visible:
                output_error_field.visible = False
                page.update()

    return on_change


def activate_on_checkbox_change(text_field: ft.TextField, page: ft.Page):
    def on_change(e):
        if text_field.disabled:
            text_field.disabled = False
        else:
            text_field.disabled = True
        page.update()

    return on_change
