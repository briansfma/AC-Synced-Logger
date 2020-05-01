##############################################################
# Brian Ma
# AC Logger: Synchronized datalogging w/ frame capture for
#            use with neural network training
#
# To activate create a folder with the same name as this file
# in apps/python. Ex apps/python/tutorial01
# Then copy this file inside it and launch AC
##############################################################

import sys
import ac
import acsys

from lib.car_inputs import InputReadout
from lib.car_g import GReadout
from lib.car_speed import SpeedReadout
from lib.track_times import LaptimeReadout

appWindow = 0
car_inputs = 0
car_g = 0
car_speed = 0
track_times = 0

def acMain(ac_version):
    global appWindow, car_inputs, car_g, car_speed, track_times

    # Start new application in session
    appWindow = ac.newApp("SyncLogger")
    ac.setSize(appWindow, 500, 100)
    
    # Print initial log confirmation
    ac.log("SyncLogger says hi!")
    ac.console("SyncLogger says hi!")
    
    # Init individual readouts
    car_inputs = InputReadout(appWindow, 3, 30)
    car_g = GReadout(appWindow, 3, 48)
    car_speed = SpeedReadout(appWindow, 3, 66)
    track_times = LaptimeReadout(appWindow, 3, 84)
    
    return "SyncLogger"

def acUpdate(deltaT):
    global car_inputs, car_g, car_speed, track_times
    
    car_inputs.update()
    car_g.update()
    car_speed.update()
    track_times.update()
