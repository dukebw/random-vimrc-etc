#!/bin/bash
bluetoothctl -- remove 60:AB:D2:EC:8D:CB
sleep 5
bluetoothctl -- pair 60:AB:D2:EC:8D:CB
sleep 5
bluetoothctl -- connect 60:AB:D2:EC:8D:CB
