import typing
from typing import Callable
import flet as ft

from enums import Currency

if typing.TYPE_CHECKING:
    from custom_classes import (
        ErrorsContainer,
        TextFieldsContainer,
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


def some_test_on_click(e):
    a = 1
    pass
