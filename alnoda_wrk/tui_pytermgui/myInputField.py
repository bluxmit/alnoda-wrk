import pytermgui as ptg

import string
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Iterator

from pytermgui.ansi_interface import MouseAction, MouseEvent
from pytermgui.enums import HorizontalAlignment
from pytermgui.helpers import break_line
from pytermgui.input import keys
from pytermgui.widgets.base import Widget


class myInputField(ptg.InputField):
    
    def handle_key(  # pylint: disable=too-many-return-statements, too-many-branches
        self, key: str
    ) -> bool:
        """Adds text to the field, or moves the cursor."""

        if self.execute_binding(key, ignore_any=True):
            return True

        for name, options in self.keys.items():
            if (
                name.rsplit("_", maxsplit=1)[-1] in ("up", "down")
                and not self.multiline
            ):
                continue

            if key in options:
                return self.handle_action(name)

        if key == keys.TAB:
            if not self.multiline:
                return False

            for _ in range(self.tablength):
                self.handle_key(" ")

            return True

        if key in string.printable and key not in "\x0c\x0b":
            if key == keys.ENTER:
                if not self.multiline:
                    return False
                try:
                    line = self._lines[self.cursor.row]
                    left, right = line[: self.cursor.col], line[self.cursor.col :]

                    self._lines[self.cursor.row] = left
                    self._lines.insert(self.cursor.row + 1, right)

                    self.move_cursor((1, -self.cursor.col))
                    self._styled_cache = None
                except:
                    pass
            else:
                self.insert_text(key)

            if keys.ANY_KEY in self._bindings:
                method, _ = self._bindings[keys.ANY_KEY]
                method(self, key)

            return True

        if key == keys.BACKSPACE:
            if self._selection_length == 1:
                self.delete_back(1)
            else:
                self.delete_back(-self._selection_length)

            # self.handle_action("move_left")

            # if self._selection_length == 1:

            self._selection_length = 1
            self._styled_cache = None

            return True

        return False



    
    def get_lines(self):
        """Builds the input field's lines."""

        if not self._cache_is_valid() or self._styled_cache is None:
            self._styled_cache = self._style_and_break_lines()

        lines = self._styled_cache

        row, col = self.cursor

        if len(self._lines) == 0:
            line = " "
        else:
            try:
                line = self._lines[row]
            except:
                # line = self._lines[len(self._lines) - 1]
                line = " "

        start = col
        cursor_char = " "
        if len(line) > col:
            start = col
            end = col + self._selection_length
            start, end = sorted([start, end])

            try:
                cursor_char = line[start:end]
            except IndexError as error:
                raise ValueError(f"Invalid index in {line!r}: {col}") from error

        style_cursor = (
            self.styles.value if self.selected_index is None else self.styles.cursor
        )

        # TODO: This is horribly hackish, but is the only way to "get around" the
        #       limits of the current scrolling techniques. Should be refactored
        #       once a better solution is available
        if self.parent is not None and self.selected_index is not None:
            offset = 0
            parent = self.parent
            while hasattr(parent, "parent"):
                offset += getattr(parent, "_scroll_offset")

                parent = parent.parent  # type: ignore

            offset_row = -offset + row
            offset_col = start + (len(self.prompt) if row == 0 else 0)

            if offset_col > self.width - 1:
                offset_col -= self.width
                offset_row += 1
                row += 1

                if row >= len(lines):
                    lines.append(self.styles.value(""))

            position = (
                self.pos[0] + offset_col,
                self.pos[1] + offset_row,
            )

            self.positioned_line_buffer.append(
                (position, style_cursor(cursor_char))  # type: ignore
            )

        lines = lines or [""]
        self.height = len(lines)

        return lines