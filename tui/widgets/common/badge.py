from textual import events
from textual.app import ComposeResult
from textual.widget import Widget


class Badge(Widget):
    DEFAULT_CSS = """
    Badge {
        width: auto;
        color: auto 80%;
        padding: 0 1;
    }
    """

    def __init__(self, *, label: str, color: str):
        self.label = label
        self.color = color
        super().__init__()

    def _on_mount(self, event: events.Mount) -> None:
        self.styles.background = self.color

    def render(self) -> ComposeResult:
        return self.label
