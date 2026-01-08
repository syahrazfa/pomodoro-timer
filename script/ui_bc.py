import tkinter as tk
from chronos import Chronos

SIZE = 320
CENTER = SIZE // 2
RADIUS = 120

STATE_COLOR = {
    Chronos.FOCUS: "#c084fc",
    Chronos.BREAK: "#38bdf8",
    Chronos.LONG_BREAK: "#fb7185",
    Chronos.IDLE: "#3f3f46"
}

class BlackChamber:
    def __init__(self, chronos: Chronos):
        self.chronos = chronos

        self.root = tk.Tk()
        self.root.configure(bg="black")
        self.root.title("MONARCH")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=SIZE, height=SIZE,
                                bg="black", highlightthickness=0)
        self.canvas.pack()

        # Aura rings (persistent)
        self.ring_active = self.canvas.create_arc(0,0,0,0)
        self.ring_shadow = self.canvas.create_arc(0,0,0,0)

        # Center display
        self.state_text = self.canvas.create_text(
            CENTER, CENTER - 30,
            fill="#a78bfa", font=("Segoe UI", 18, "bold")
        )

        self.time_text = self.canvas.create_text(
            CENTER, CENTER + 2,
            fill="white", font=("Consolas", 36, "bold")
        )

        self.cycle_text = self.canvas.create_text(
            CENTER, CENTER + 40,
            fill="#71717a", font=("Segoe UI", 12)
        )

        # Control panel
        panel = tk.Frame(self.root, bg="black")
        panel.pack(pady=12)

        self.start_btn = tk.Button(
            panel, text="⏳ START", command=self.chronos.start,
            bg="#7c3aed", fg="white", relief="flat",
            activebackground="#5b21b6", width=10
        )
        self.start_btn.grid(row=0, column=0, padx=8)

        self.idle_btn = tk.Button(
            panel, text="☠ IDLE", command=self.chronos.idle,
            bg="#27272a", fg="#a1a1aa", relief="flat",
            activebackground="#18181b", width=10
        )
        self.idle_btn.grid(row=0, column=1, padx=8)

        chronos.subscribe(self.on_event)
        self.frame()

    # Chronos lifecycle events
    def on_event(self, event, state):
        self.update_center()

    # Single authoritative render loop
    def frame(self):
        self.chronos.tick()
        self.update_center()
        self.draw_ring()
        self.root.after(250, self.frame)

    # Center HUD
    def update_center(self):
        sec = self.chronos.remaining()
        self.canvas.itemconfig(self.state_text, text=self.chronos.state)
        self.canvas.itemconfig(self.time_text, text=f"{sec//60:02}:{sec%60:02}")
        self.canvas.itemconfig(self.cycle_text,
                               text=f"Cycle {self.chronos.cycle_count % 4}/4")

    # Aura ring engine
    def draw_ring(self):
        total = self.get_total_seconds()
        remaining = self.chronos.remaining()

        if total == 0:
            self.canvas.itemconfig(self.ring_active, extent=0)
            self.canvas.itemconfig(self.ring_shadow, extent=360)
            return

        pct = remaining / total
        angle = pct * 360
        color = STATE_COLOR[self.chronos.state]

        self.canvas.coords(self.ring_active,
            CENTER-RADIUS, CENTER-RADIUS, CENTER+RADIUS, CENTER+RADIUS)
        self.canvas.coords(self.ring_shadow,
            CENTER-RADIUS, CENTER-RADIUS, CENTER+RADIUS, CENTER+RADIUS)

        self.canvas.itemconfig(self.ring_active,
            start=90, extent=-angle, style="arc", width=18, outline=color)

        self.canvas.itemconfig(self.ring_shadow,
            start=90-angle, extent=-(360-angle), style="arc",
            width=18, outline="#18181b")

    def get_total_seconds(self):
        if self.chronos.state == Chronos.FOCUS:
            return self.chronos.focus_min * 60
        if self.chronos.state == Chronos.BREAK:
            return self.chronos.break_min * 60
        if self.chronos.state == Chronos.LONG_BREAK:
            return self.chronos.long_break_min * 60
        return 0

    def run(self):
        self.root.mainloop()
