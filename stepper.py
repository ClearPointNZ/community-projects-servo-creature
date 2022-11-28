#!/usr/bin/env python3
from time import sleep
from math import floor as m_floor
import getch as gh
# Swap line 7 for lines 5,6 if not on a Pi
import fake_rpi.RPi as FRPi
GPIO = FRPi.GPIO
# import RPi.GPIO as GPIO


DEGREES = 360
REVERSE = False

IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
pins = [IN1, IN2, IN3, IN4]

sleep_duration = 0.001

# Half step sequence
# This is smoother and quieter, can be an extension
half_sequence = [[1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1],
                 [1, 0, 0, 1]]

step_sequence = half_sequence

def init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)


def cycle(sequence):
    for i in range(len(sequence)):
        for j in range(len(pins)):
            GPIO.output(pins[j], sequence[i][j])
        sleep(sleep_duration)


def step(steps=1, reverse=False):
    seq = step_sequence

    if reverse:
        seq = seq[::-1]

    for i in range(steps):
        cycle(seq)


def degrees_to_steps(degrees=360):
    return m_floor(degrees / (5.625 * (1 / 64)))


init()

try:
    step(degrees_to_steps(DEGREES), REVERSE)
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)

GPIO.cleanup()
exit(0)
