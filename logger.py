##############################################################
# Brian Ma
# AC Logger: Synchronized datalogging w/ frame capture for
#            use with neural network training
#
# To activate, copy everything in this repository into
# "apps/python/logger/" in your main Assetto Corsa directory.
##############################################################

import sys
import os
import platform
import csv
import ac
import acsys

# Fix import path for ctypes (needed for mss and track_times)
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

csvfile = 0
writer = 0
sct = 0
monitor = 0
recording = False
recButton = 0
seq_num = 0
frame_num = 0

mon_select = 2
folder = "apps/python/logger/captures/" # set dir for saving images

def toggle(dummy, var):
    global recording, seq_num, frame_num, recButton
    
    if recording:
        recording = False
        ac.setText(recButton, "Start Recording")
    else:
        recording = True
        seq_num += 1
        frame_num = 1
        ac.setText(recButton, "Stop Recording")

def acMain(ac_version):
    global appWindow, car_inputs, car_g, car_speed, track_times, perf_delta
    global csvfile, writer
    global sct, mon_select, monitor, recButton

    # Start new application in session
    appWindow = ac.newApp("SyncLogger")
    ac.setSize(appWindow, 200, 50)
    
    # Print initial log confirmation
    ac.log("SyncLogger says hi!")
    ac.console("SyncLogger says hi!")
    
    # Init individual readouts
    #   Number values are for x/y positioning of readouts if enabled
    car_inputs = InputReadout(appWindow, 3, 30)
    car_g = GReadout(appWindow, 3, 48)
    car_speed = SpeedReadout(appWindow, 3, 66)
    track_times = LaptimeReadout(appWindow, 3, 84)
    perf_delta = DeltaReadout(appWindow, 3, 102)
    
    # Init screen reader object
    sct = mss.mss()
    monitor = sct.monitors[mon_select]  # select monitor
    
    recButton = ac.addButton(appWindow, "Start Recording")
    ac.setPosition(recButton, 0, 30)
    ac.setSize(recButton, 200, 20)
    ac.addOnClickedListener(recButton, toggle)
    
    csvfile = open(folder + 'data.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    
    return "SyncLogger"

def acUpdate(deltaT):
    global car_inputs, car_g, car_speed, track_times, perf_delta
    global writer
    global sct, folder, monitor, recording, seq_num, frame_num
    
    if recording:
        # Grab data
        gas, brake, clutch, gear, steer = car_inputs.update()
        lat_g, lon_g = car_g.update()
        speed = car_speed.update()
        lap_valid, curr_lap, best_lap = track_times.update()
        pos, p_meter, p_rate = perf_delta.update(deltaT)
        
        # Grab screen frame
        im = sct.grab(monitor)          # type: ignore
        
        # Save screen frame in captures folder (PNG)
        filename = "{:02d}_{:06d}.png".format(seq_num, frame_num)
        mss.tools.to_png(im.rgb, im.size, output=(folder + filename))
        frame_num += 1
        
        # Save data in captures folder (CSV)
        writer.writerow([filename,
                         round(gas, 2), round(brake, 2), round(clutch, 1), 
                         round(gear, 0), round(steer, 0),
                         round(lat_g, 2), round(lon_g, 2), round(speed, 1),
                         lap_valid, round(curr_lap/1000, 2), round(best_lap/1000, 2),
                         round(pos, 5), p_meter, p_rate])

def acShutdown():
    global csvfile
    
    csvfile.close()
