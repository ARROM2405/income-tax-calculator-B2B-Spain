from __future__ import annotations

from abc import ABC

import flet as ft
import flet_core
from flet_core import FontWeight

from utils import validate_text_field_numeric, validate_text_field
from typing import Container, Iterable


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
        self.text_field = text_field
        self.error = error

    @classmethod
    def get_field_with_added_error(
        cls,
        *args,
        validation_numeric_type: type(int) | type(float),
        errors_container: ErrorsContainer,
        text_fields_container: TextFieldsContainer,
        submit_button: EnhancedElevatedButton,
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
        errors_container.add_member(error)
        text_field = ft.TextField(
            *args,
            on_change=validate_text_field(
                error,
                submit_button,
                page,
                validation_numeric_type,
            ),
            **kwargs,
        )
        text_fields_container.add_member(text_field)
        return cls(text_field=text_field, error=error)


class ItemsContainer(ABC):
    MEMBERS_CLASS = None

    def __init__(self, *items):
        self._members = list(items)

    def add_members(self, *items: Iterable[MEMBERS_CLASS]):
        self._members.extend(items)

    def add_member(self, item: MEMBERS_CLASS):
        self._members.append(item)


class ErrorsContainer(ItemsContainer):
    MEMBERS_CLASS = ft.Text

    def enabled_errors_exist(self):
        enabled_errors = [error for error in self._members if error.visible]
        return len(enabled_errors) > 0

    @property
    def errors(self):
        return self._members


class TextFieldsContainer(ItemsContainer):
    MEMBERS_CLASS = ft.TextField

    def all_endabled_fields_have_value(self):
        empty_enabled_text_fields = [
            text_field
            for text_field in self._members
            if text_field.value in ("", None) and text_field.disabled is False
        ]
        return len(empty_enabled_text_fields) == 0


class EnhancedElevatedButton(ft.ElevatedButton):
    def __init__(
        self,
        *args,
        depend_on_error_fields: ErrorsContainer,
        depend_on_text_fields: TextFieldsContainer,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.depend_on_error_fields = depend_on_error_fields
        self.depend_on_text_fields = depend_on_text_fields

    @property
    def has_to_be_disabled(self) -> bool:
        if self.depend_on_error_fields.enabled_errors_exist():
            return True
        if not self.depend_on_text_fields.all_endabled_fields_have_value():
            return True
        return False

    def disability_update(self):
        if self.disabled != self.has_to_be_disabled:
            self.disabled = self.has_to_be_disabled
