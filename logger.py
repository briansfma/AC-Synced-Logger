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

from lib.car_g import GReadout

appWindow = 0
car_g = 0

def acMain(ac_version):
    global appWindow, car_g

    appWindow = ac.newApp("SyncLogger")
    ac.setSize(appWindow, 200, 100)
    
    ac.log("SyncLogger says hi!")
    ac.console("SyncLogger says hi!")
    
    car_g = GReadout(appWindow, 3, 30)
    
    return "SyncLogger"

def acUpdate(deltaT):
    global car_g
    
    car_g.update()
