from typing import Any

from textual import widgets
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Static


class VerticalScrollSelectListItem(Static):
    def __init__(self, item: Any, item_widget: widgets) -> None:
        self.item = item
        self.item_widget = item_widget
        super().__init__()

    class ItemClicked(Message):
        """Sent when an item from the list is clicked"""

        def __init__(self, item: Any) -> None:
            self.item = item
            super().__init__()

    def on_click(self) -> None:
        self.post_message(self.ItemClicked(self.item))

    def compose(self) -> ComposeResult:
        yield self.item_widget(self.item)
