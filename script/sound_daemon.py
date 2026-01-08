import winsound
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
TRANSITION = str(ASSETS / "transition.wav")

class MonarchSound:
    def __init__(self, chronos):
        chronos.subscribe(self.on_event)

    def on_event(self, event, state):
        if event in (
            "on_focus_start",
            "on_focus_end",
            "on_break_start",
            "on_long_break_start",
        ):
            winsound.PlaySound(TRANSITION, winsound.SND_FILENAME | winsound.SND_ASYNC)
