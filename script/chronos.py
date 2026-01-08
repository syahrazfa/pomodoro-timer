import time

class Chronos:
    FOCUS = "FOCUS"
    BREAK = "BREAK"
    LONG_BREAK = "LONG_BREAK"
    IDLE = "IDLE"

    def __init__(self, focus_min=25, break_min=5, long_break_min=15):
        self.focus_min = focus_min
        self.break_min = break_min
        self.long_break_min = long_break_min
        self.cycle_count = 0
        self.state = self.IDLE
        self._mono_end = None
        self.subscribers = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def _emit(self, event):
        for fn in self.subscribers:
            fn(event, self.state)

    def start(self):
        self._set_state(self.FOCUS)

    def idle(self):
        self._set_state(self.IDLE)

    def _set_state(self, state):
        prev = self.state
        self.state = state

        if state == self.FOCUS:
            self._mono_end = time.monotonic() + self.focus_min * 60
        elif state == self.BREAK:
            self._mono_end = time.monotonic() + self.break_min * 60
        elif state == self.LONG_BREAK:
            self._mono_end = time.monotonic() + self.long_break_min * 60
        else:
            self._mono_end = None

        if prev == self.FOCUS and state != self.FOCUS:
            self._emit("on_focus_end")
        if prev == self.BREAK and state != self.BREAK:
            self._emit("on_break_end")
        if prev == self.LONG_BREAK and state != self.LONG_BREAK:
            self._emit("on_long_break_end")

        if state == self.FOCUS:
            self._emit("on_focus_start")
        if state == self.BREAK:
            self._emit("on_break_start")
        if state == self.LONG_BREAK:
            self._emit("on_long_break_start")

    def tick(self):
        if self.state == self.IDLE or self._mono_end is None:
            return

        if time.monotonic() >= self._mono_end:
            if self.state == self.FOCUS:
                self.cycle_count += 1
                if self.cycle_count % 4 == 0:
                    self._set_state(self.LONG_BREAK)
                else:
                    self._set_state(self.BREAK)
            else:
                self._set_state(self.FOCUS)

    def remaining(self):
        if self._mono_end is None:
            return 0
        return max(int(self._mono_end - time.monotonic()), 0)
