# Script to handle acquisition of car G-force data

import ac
import acsys

# Parameters
filter = 0.2

class GReadout:
    def __init__(self, appWindow, x, y):
        # Init containers for low-pass filtering of raw data
        self.currentLatG = 0
        self.currentLonG = 0
        self.oldLatG = 0
        self.oldLonG = 0

        # # Init and display labels for lateral, longitudinal G's
        # self.l_lat_g = ac.addLabel(appWindow, "Lat. G: 0.00");
        # ac.setPosition(self.l_lat_g, x, y)
        # self.l_lon_g = ac.addLabel(appWindow, "Lon. G: 0.00");
        # ac.setPosition(self.l_lon_g, x+100, y)
    
    def update(self):
        global filter
        
        x, y, z = ac.getCarState(0, acsys.CS.AccG)
        
        self.currentLatG = self.oldLatG * filter + x * (1-filter)
        self.currentLonG = self.oldLonG * filter + z * (1-filter)
        
        self.oldLatG = self.currentLatG
        self.oldLonG = self.currentLonG

        # # Update labels
        # ac.setText(self.l_lat_g, "Lat. G: {:04.2f}".format(self.currentLatG))
        # ac.setText(self.l_lon_g, "Lon. G: {:04.2f}".format(self.currentLonG))
        
        return self.currentLatG, self.currentLonG
