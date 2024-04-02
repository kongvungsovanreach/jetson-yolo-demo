#!/bin/bash

cd /home/nvidia/Desktop/jetson-demo && export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstnvvidconv.so && /usr/bin/python3 run_yolo_gpio.py
