#!/usr/bin/python
# coding=utf-8

#running program with 'python3'
#couchdb server should boot up automatically
#if the database is down, try => sudo -i -u couchdb /home/couchdb/bin/couchdb
#if even that doesn't work, reinstall couchdb with 'sudo pip3 install couchdb'
#couchdb user-interface default url: http://localhost:5984/_utils/#database/joystick/_all_docs
#for adafruit funcionaltiy, adafruit_ads1x15 library has to be in the same folder as this script

import pycouchdb
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#PIN settings
Button_PIN = 24
Buzzer_PIN = 27

#PIN setup for buzzer sound
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)

#PIN setup for Joystick-Button
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.input(Button_PIN)==True     -> query if button/joystick is pressed

#time period for loop -> when joystick is held longer in one direction, just every 1 second a signal is sent
delayTime = 1

# Create the I2C bus
# normally, GPIO PINS aren't in SCL/SDA mode, if this programm doesn'T work try switching on the SDA/SCL mode in the raspy-config
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

#couchdb server host setup
couch = pycouchdb.Server("http://localhost:5984/")
#couchdb database setup
db = couch.database('joystick')

#generates buzzer sound
def buzzern():
    GPIO.output(Buzzer_PIN, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(Buzzer_PIN, GPIO.LOW)

#actions when joystick movement happens
def movement(direction):
    buzzern()
    obj = db.get('dirID')
    obj['dir'] = direction
    db.save(obj)
    time.sleep(delayTime)

while True:
                #reading the analog signals
                x = chan0.value
                y = chan1.value
                
		#the if numbers are values from 0 to 30000
		#if the joystick stands still, the default input is ~20800
                if x < 5000: #joystick down-move
                    movement("down")
                    continue
                if x > 28000: #joystick up-move
                    movement("up")
                    continue
                if y < 5000: #joystick right-move
                    movement("right")
                    continue
                if y > 28000: #joystick left-move
                    movement("left")
                    continue
                if GPIO.input(Button_PIN)==True:
                    movement("pressed")
                    continue