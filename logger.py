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
import os
import platform
import ac
import acsys

# Fix import path for ctypes (needed for sim_info and screen recording)
if platform.architecture()[0] == "64bit":
    sysdir = 'apps/python/logger/stdlib64'
else:
    sysdir = 'apps/python/logger/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] += ";."

import lib.mss as mss
from lib.car_inputs import InputReadout
from lib.car_g import GReadout
from lib.car_speed import SpeedReadout
from lib.track_times import LaptimeReadout
from lib.perf_delta import DeltaReadout

appWindow = 0
car_inputs = 0
car_g = 0
car_speed = 0
track_times = 0
perf_delta = 0
sct = 0

recording = False
recStatus = 0
frame_num = 0

def toggle(dummy, var):
    global recording
    
    if recording:
        recording = False
    else:
        recording = True
    
    ac.setText(recStatus, "Recording? {}".format(recording))

def acMain(ac_version):
    global appWindow, car_inputs, car_g, car_speed, track_times, perf_delta
    global sct, recording, recStatus, frame_num

    # Start new application in session
    appWindow = ac.newApp("SyncLogger")
    ac.setSize(appWindow, 500, 160)
    
    # Print initial log confirmation
    ac.log("SyncLogger says hi!")
    ac.console("SyncLogger says hi!")
    
    # Init individual readouts
    car_inputs = InputReadout(appWindow, 3, 30)
    car_g = GReadout(appWindow, 3, 48)
    car_speed = SpeedReadout(appWindow, 3, 66)
    track_times = LaptimeReadout(appWindow, 3, 84)
    perf_delta = DeltaReadout(appWindow, 3, 102)
    
    sct = mss.mss()
    
    recButton = ac.addButton(appWindow, "Start Recording")
    ac.setPosition(recButton, 150, 135)
    ac.setSize(recButton, 200, 20)
    ac.addOnClickedListener(recButton, toggle)
    
    recStatus = ac.addLabel(appWindow, "Recording? {}".format(recording))
    ac.setPosition(recStatus, 3, 135)
    
    frame_num = 1
    
    return "SyncLogger"

def acUpdate(deltaT):
    global car_inputs, car_g, car_speed, track_times, perf_delta
    global sct, recording, recStatus, frame_num
    
    if recording:
        car_inputs.update()
        car_g.update()
        car_speed.update()
        track_times.update()
        perf_delta.update(deltaT)
        
        # Grab screen
        monitor = sct.monitors[2]       # Use the 1st monitor

        # Grab the picture
        im = sct.grab(monitor)          # type: ignore

        # TODO: correct file name LMAO
        filepath = "apps/python/logger/captures/{:06d}.png".format(frame_num)
        mss.tools.to_png(im.rgb, im.size, output=filepath)
        
        frame_num += 1
