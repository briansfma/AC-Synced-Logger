# Script to handle acquisition of car G-force data

import ac
import acsys

class InputReadout:
    def __init__(self, appWindow, x, y):
        # Init containers for low-pass filtering of raw data
        self.gas = 0
        self.brake = 0
        self.clutch = 0
        self.gear = 0
        self.steer = 0

        # Init and display labels for lateral, longitudinal G's
        self.l_gas = ac.addLabel(appWindow, "Gas: 0.00");
        ac.setPosition(self.l_gas, x, y)
        self.l_brake = ac.addLabel(appWindow, "Brake: 0.00");
        ac.setPosition(self.l_brake, x+100, y)
        self.l_clutch = ac.addLabel(appWindow, "Clutch: 0.00");
        ac.setPosition(self.l_clutch, x+200, y)
        self.l_gear = ac.addLabel(appWindow, "Gear: 0");
        ac.setPosition(self.l_gear, x+300, y)
        self.l_steer = ac.addLabel(appWindow, "Steer: 0.00");
        ac.setPosition(self.l_steer, x+400, y)
    
    def update(self):        
        self.gas = ac.getCarState(0, acsys.CS.Gas)
        self.brake = ac.getCarState(0, acsys.CS.Brake)
        self.clutch = ac.getCarState(0, acsys.CS.Clutch)
        self.gear = ac.getCarState(0, acsys.CS.Gear) - 1
        self.steer = ac.getCarState(0, acsys.CS.Steer)

        ac.setText(self.l_gas, "Gas: {:04.2f}".format(self.gas))
        ac.setText(self.l_brake, "Brake: {:04.2f}".format(self.brake))
        ac.setText(self.l_clutch, "Clutch: {:04.2f}".format(self.clutch))
        ac.setText(self.l_gear, "Gear: {:01d}".format(self.gear))
        ac.setText(self.l_steer, "Steer: {:04.2f}".format(self.steer))
