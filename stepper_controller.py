#!/usr/bin/env python
import math
import time
import controller
# Swap the lines below with the one commented further down if editing code on a Pi
import fake_rpi.RPi as FRPi
GPIO = FRPi.GPIO
# import RPi.GPIO as GPIO

# Update these to match the GPIO pins the stepper motor controller is connected to
# Currently setup for a Pi model b+
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
pins = [IN1, IN2, IN3, IN4]

# Tweak this step faster or slower, too fast and the motor won't turn
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

# Step sequence
norm_sequence = [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]]

step_sequence = half_sequence


def init():
    """
    Initialises the GPIO pins specified above by:
    * Setting the numbering mode to use Broadcom numbering
    * Setting the 4 pins as outputs
    * Resetting all the outputs to False so that the motor is idle
    """
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)


def run_sequence(sequence):
    """
    Run through a given sequence ONCE, pausing for `sleep_duration` between each phase of the sequence
    :param sequence: a list of 4 element lists with the state of each pin in order
    """
    for i in range(len(sequence)):
        for j in range(len(pins)):
            GPIO.output(pins[j], sequence[i][j])
        time.sleep(sleep_duration)


def reset_pins():
    """
    Reset all 4 of the motor output pins to off
    """
    GPIO.output(IN1, False)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, False)


def step(steps=1, reverse=False):
    """
    Run through the chosen sequence `steps` number of times
    :param steps: How many iterations to run of the sequence
    :param reverse: Run the sequence in reverse, turns the motor the other way
    """
    seq = step_sequence

    if reverse:
        seq = seq[::-1]

    for i in range(steps):
        run_sequence(seq)


def degrees_to_steps(degrees=360):
    """
    Return the number of sequence iterations required to rotate the motor by the given amount in degrees
    """
    return math.floor(degrees / (5.625 * (1 / 64)))


init()
xbox_controller = controller.XboxController()

try:
    # Infinite loop waiting for controller inputs
    while True:
        [left, right] = xbox_controller.read()
        if left:
            step(degrees_to_steps(1), False)
        elif right:
            step(degrees_to_steps(1), True)
        else:
            reset_pins()
except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)

GPIO.cleanup()
exit(0)
