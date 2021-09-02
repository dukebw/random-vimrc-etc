#!/bin/bash
bluetoothctl remove 60:AB:D2:EC:8D:CB
bluetoothctl scan on
bluetoothctl trust 60:AB:D2:EC:8D:CB
bluetoothctl pair 60:AB:D2:EC:8D:CB
bluetoothctl connect 60:AB:D2:EC:8D:CB
