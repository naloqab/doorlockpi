import time

import RPi.GPIO as GPIO



GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)


delay  = delay0   = 0.0001

#delay = delay90  = 0.0016

#delay = delay180 = 0.0022



for x in xrange(0, 50):
        
	GPIO.output(4, 1)
        
	time.sleep(delay)
        
	GPIO.output(4, 0)
        
	time.sleep(0.02-delay)

