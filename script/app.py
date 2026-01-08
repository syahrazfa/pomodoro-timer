from sound_daemon import MonarchSound
from chronos import Chronos
from ui_bc import BlackChamber

clock = Chronos(focus_min=25, break_min=5, long_break_min=15)
MonarchSound(clock)
BlackChamber(clock).run()
