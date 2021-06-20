#!/bin/bash
{
        printf 'remove 60:AB:D2:EC:8D:CB'
        printf 'scan on'
        sleep 5
        printf 'connect 60:AB:D2:EC:8D:CB'
} | bluetoothctl
