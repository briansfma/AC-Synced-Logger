# Script to handle acquisition of car G-force data

import sys
import os
import platform
import ac
import acsys

# Fix import path for ctypes (needed for sim_info)
if platform.architecture()[0] == "64bit":
    sysdir = 'apps/python/logger/stdlib64'
else:
    sysdir = 'apps/python/logger/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] += ";."

from sim_info import info

# Parameters
tireOffLimit = 3

class LaptimeReadout:
    def __init__(self, appWindow, x, y):
        # Init containers
        self.lapCount = 0
        self.bestLap = 0
        self.bestLapNum = 0
        self.lastLap = 0
        self.currentLap = 0
        self.lapValid = True
        
        ac.console("Lap valid? {}".format(self.lapValid))

        # Init and display labels for best, last and current lap
        self.l_bestLap = ac.addLabel(appWindow, "Best Lap: 0:00.0");
        ac.setPosition(self.l_bestLap, x, y)
        self.l_lastLap = ac.addLabel(appWindow, "Last Lap: 0:00.0");
        ac.setPosition(self.l_lastLap, x+150, y)
        self.l_currentLap = ac.addLabel(appWindow, "Current Lap: 0:00.0 (I)");
        ac.setPosition(self.l_currentLap, x+300, y)
    
    def convertMS(self, millis):
        tenths = int((millis/100)%10)
        seconds = int((millis/1000)%60)
        minutes = int(millis/(1000*60))
        
        return minutes, seconds, tenths
    
    def update(self):
        # Constantly monitor if car has cut the track (lap invalid)
        global tireOffLimit
        offTrack = info.physics.numberOfTyresOut > tireOffLimit
        if offTrack:
            self.lapValid = False
            ac.console("Lap valid? {}".format(self.lapValid))
        
        # Get and update current lap time
        self.currentLap = ac.getCarState(0, acsys.CS.LapTime)
        mins, secs, tenths = self.convertMS(self.currentLap)
        
        ac.setText(self.l_currentLap, 
                   "Current Lap: {:d}:{:02d}.{:1d} ({})"
                   .format(mins, secs, tenths, self.lapValid))
        
        # Update lap count only when it happens
        laps = ac.getCarState(0, acsys.CS.LapCount)
        if (laps > self.lapCount):
            self.lapCount += 1
            
            self.lastLap = ac.getCarState(0, acsys.CS.LastLap)
            mins, secs, tenths = self.convertMS(self.lastLap)
                    
            ac.setText(self.l_lastLap, 
                       "Last Lap: {:d}:{:02d}.{:1d} ({})"
                       .format(mins, secs, tenths, self.lapValid))
            
            # Compare last lap to best lap only if valid
            if ((self.lastLap < self.bestLap or self.bestLap == 0)
              and self.lapValid):
                self.bestLapNum = laps
                self.bestLap = self.lastLap
                
                ac.setText(self.l_bestLap, 
                           "Best Lap: {:d}:{:02d}.{:1d} ({:d})"
                           .format(mins, secs, tenths, self.bestLapNum))

