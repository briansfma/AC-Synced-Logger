# Script to handle acquisition/calc of performance delta

import ac
import acsys

# Parameters
filter = 0.2

class DeltaReadout:
    def __init__(self, appWindow, x, y):
        # Init containers for low-pass filtering of raw data
        self.pos = 0
        self.oldPos = 0
        self.meter = 0
        self.oldMeter = 0

        # Init and display labels for lateral, longitudinal G's
        self.l_pos = ac.addLabel(appWindow, "Spline Pos: 0.00");
        ac.setPosition(self.l_pos, x, y)
        self.l_meter = ac.addLabel(appWindow, "Perf Meter: 0.00");
        ac.setPosition(self.l_meter, x+150, y)
        self.l_rate = ac.addLabel(appWindow, "Perf Gain Rate: 0.00");
        ac.setPosition(self.l_rate, x+300, y)
    
    def update(self, deltaT):
        global filter
        
        newPos = ac.getCarState(0, acsys.CS.NormalizedSplinePosition)
        self.pos = self.oldPos * filter + newPos * (1-filter)
        self.oldPos = self.pos
        
        newMeter = ac.getCarState(0, acsys.CS.PerformanceMeter)
        self.meter = self.oldMeter * filter + newMeter * (1-filter)
        rate = (self.oldMeter - self.meter)/deltaT
        self.oldMeter = self.meter

        ac.setText(self.l_pos, "Spline Pos: {:06.4f}".format(self.pos))
        ac.setText(self.l_meter, "Perf Meter: {:06.4f}".format(self.meter))
        ac.setText(self.l_rate, "Perf Gain Rate: {:06.4f}".format(rate))
