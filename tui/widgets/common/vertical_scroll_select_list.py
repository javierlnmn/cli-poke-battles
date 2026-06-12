from typing import Any

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widget import Widget

from tui.widgets.common.vertical_scroll_select_list_item import VerticalScrollSelectListItem


class VerticalScrollSelectList(Widget):
    def __init__(self, items_list: list[Any], item_widget: Widget):
        self.items_list = items_list
        self.item_widget = item_widget
        super().__init__()

    class ItemClicked(Message):
        """Sent when an item from the list is clicked"""

        def __init__(self, item: Any) -> None:
            super().__init__()
            self.item = item

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for item in self.items_list:
                yield VerticalScrollSelectListItem(
                    item=item,
                    item_widget=self.item_widget,
                )

    def on_vertical_scroll_select_list_item_item_clicked(
        self, message: VerticalScrollSelectListItem.ItemClicked
    ):
        self.post_message(self.ItemClicked(message.item))
