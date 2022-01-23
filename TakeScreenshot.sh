#!/bin/bash

x=$(xdotool getactivewindow)
xdotool windowminimize $x
sleep 1
xdotool windowactivate $x