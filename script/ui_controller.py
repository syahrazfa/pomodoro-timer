class UIController:
    def __init__(self, chronos):
        self.chronos = chronos
        chronos.subscribe(self.on_event)

        self.state = chronos.state
        self.remaining = chronos.remaining()

    def on_event(self, event, state):
        self.state = state
        self.remaining = self.chronos.remaining()
