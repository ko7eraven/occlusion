#!/bin/sh

make monitor | grep "MOTOR: Motor duty" > motor.txt

