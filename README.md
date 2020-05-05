# Assetto Corsa Synchronized Frame/Telemetry Logger

This utility outputs time-aligned frame captures and telemetry data from the racing simulator Assetto Corsa. You can do whatever you like with the data, including analyzing it for your own driver development, but the intent is to help users create training/validation/test data sets for developing AI driving models.

[//]: # (Image References)
[image1]: example.png "Runtime Example"
[image2]: data_example.png "Data Example"

## Basic Build Instructions

To activate this script, clone this directory within the `apps/python` folder in your main `assettocorsa` installation directory. Then launch Assetto Corsa, enter Settings > General > scroll to the bottom and check the "logger" box to enable the app. It will be available to turn on as soon as you start a driving session.

## Usage
The logger only has one control - recording or not. You can press the "Start Recording" button at any time during a session and it will begin capturing frames and data as Assetto Corsa serves it.

![alt text][image1]

Multiple start/stop recordings are handled gracefully via filename (prefix 01_ for the first recording, 02_ for the second, etc). The outputs (image frames and data CSV file) can be found in the `captures/` folder after the session has ended. The CSV is organized as follows:

![alt text][image2]

- A) Image file
- B) Gas (Throttle) 0.0 to 1.0
- C) Brake 0.0 to 1.0
- D) Clutch 0.0 to 1.0
- E) Gear -1 (reverse) to 6 (6th)
- F) Steering wheel angle in degrees (depends on user hardware)
- G) Lateral acceleration in G
- H) Longitudinal acceleration in G
- I) Speed in MPH (only works going forward)
- J) Lap Valid? TRUE so long as car has not left the track surface
- K) Current lap time in seconds
- L) Best lap time (of current session) in seconds
- M) Proportion of lap completed 0.0 to 1.0
- N) Performance delta in seconds (negative = faster)
- O) Rate of gain of performance delta (positve = faster)

Any or all of these quantities can be used. Feature requests are welcome!

## Known issues
Because we are compressing and writing image frames alongside rendering them, frame rate in Assetto Corsa will drop during recording. This will be worked on, but please be aware of physical limitations on computing power.

## Credits
Thanks to Mickaël Schoentgen for his project [`python-mss`](https://github.com/BoboTiG/python-mss), which powers the screen grab function of this utility.