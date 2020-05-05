# Script to handle acquisition of car speed data

import ac
import acsys

# Parameters
filter = 0.2

class SpeedReadout:
    def __init__(self, appWindow, x, y):
        # Init containers for low-pass filtering of raw data
        self.currentSpeed = 0
        self.oldSpeed = 0

        # # Init and display labels for speed
        # self.l_speed = ac.addLabel(appWindow, "Speed: 0.00");
        # ac.setPosition(self.l_speed, x, y)
    
    def update(self):
        global filter
        
        s = ac.getCarState(0, acsys.CS.SpeedMPH)
        self.currentSpeed = self.oldSpeed * filter + s * (1-filter)
        
        self.oldSpeed = self.currentSpeed

        # # Update labels
        # ac.setText(self.l_speed, "Speed: {:03.1f}".format(self.currentSpeed))
        
        return self.currentSpeed
