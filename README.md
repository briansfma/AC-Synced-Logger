# Assetto Corsa Synchronized Frame/Telemetry Logger

This utility is in its very early stages. It intends to output time-aligned frame captures and telemetry data from the racing simulator Assetto Corsa so that a user can quickly organize data into a training/validation/test set for a neural network(s) based driver.

[//]: # (Image References)
[image1]: Progress2.jpg "Runtime Example"

## Basic Build Instructions

To activate this script, clone this directory within the `apps/python` folder in your main `assettocorsa` installation directory. Then launch Assetto Corsa, enter Settings > General > scroll to the bottom and check the "logger" box to enable the app. It will be available to turn on as soon as you start a driving session.

## Usage
The logger only has one control - recording or not. You can press the "Start Recording" button at any time during a session and it will begin capturing frames and data as Assetto Corsa serves it. Multiple start/stop recordings are handled gracefully via filename (prefix 01_ for the first recording, 02_ for the second, etc). The outputs (image frames and data CSV file) can be found in the `captures/` folder after the session has ended.