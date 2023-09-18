from __future__ import annotations

from collections.abc import Container
import flet as ft
import flet_core
from flet_core import FontWeight

from utils import validate_text_field_numeric


class Block:
    def __init__(self):
        self.controls = []

    def add(self, *controls: ft.Control):
        self.controls.extend(controls)

    def to_row(self, row_controls_count: int = 0, **kwargs):
        rows = []
        row = ft.Row(**kwargs)
        for control in self.controls:
            if row_controls_count and len(row.controls) >= row_controls_count:
                rows.append(row)
                row = ft.Row(**kwargs)
            row.controls.append(control)
        rows.append(row)
        self.controls = rows


class TextFieldWithErrorField:
    def __init__(
        self,
        text_field: ft.TextField,
        error: ft.Text,
    ):
        self._text_field = text_field
        self._error = error

    @classmethod
    def get_field_with_added_error(
        cls,
        *args,
        validation_numeric_type: type(int) | type(float),
        page: ft.Page,
        **kwargs,
    ) -> TextFieldWithErrorField:
        error = ft.Text(
            value="",
            weight=FontWeight.BOLD,
            visible=False,
            color=flet_core.colors.ERROR,
            text_align=flet_core.TextAlign.CENTER,
        )
        text_field = ft.TextField(
            *args,
            on_change=validate_text_field_numeric(error, page, validation_numeric_type),
            **kwargs,
        )
        return cls(text_field=text_field, error=error)

    @property
    def text_field(self):
        return self._text_field

    @property
    def error(self):
        return self._error
