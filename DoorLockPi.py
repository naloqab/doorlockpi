import RPi.GPIO as GPIO
import os
import time
import MFRC522
import socket

# Socket related
Host = '192.168.1.220'
Port = 5007

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.IN)

# Tag/Card Register
NaserTag = '85157168107'
NaserCard = '19183225213'
AmberTag = '2293343119'
AmberCard = '254244228213'

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Initial Pushbutton LED Status
StatusFile = open('/var/www/code/LockStatus.txt', 'r')
LockStatus = StatusFile.readline()
if LockStatus == 'Unlocked':
	GPIO.output(5, False)
if LockStatus == 'Locked':
	GPIO.output(5, True)
StatusFile.close()

while True:
	StatusChange = 'Unchanged'

	StatusFile = open('/var/www/code/LockStatus.txt', 'r')
	LockStatus = StatusFile.readline()
	StatusFile.close()

	# Hall Sensor
	if GPIO.input(12) == 0 and LockStatus == 'Unlocked':
		print ""
		print "Door Closed"
		os.system("sudo python /var/www/code/ServoLock.py")
		LockStatus = 'Locked'
		print "Lock Status:", LockStatus
		time.sleep(1)
		StatusChange = 'Changed'
			

	# Pushbutton Code
        if GPIO.input(3) == 0:
		print ""
		print "Button Pressed"

		if LockStatus == 'Unlocked':
			os.system("sudo python /var/www/code/ServoLock.py")
			LockStatus = 'Locked'
			print "Lock Status:", LockStatus
			time.sleep(1)
			StatusChange = 'Changed'

		elif LockStatus == 'Locked':
			os.system("sudo python /var/www/code/ServoUnlock.py")
			LockStatus = 'Unlocked'
			print "Lock Status:", LockStatus
			if time.localtime().tm_hour >= 17 or time.localtime().tm_hour < 5:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((Host, Port))
				s.sendall('1')         # Send 1 to server for the lights to turn off.
				data = s.recv(1024)
				s.close()
			time.sleep(1)
			StatusChange = 'Changed'

	# RFID Code
	# Scan for tags/cards
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# If we have the UID, continue
	UIDcode = ""
	if status == MIFAREReader.MI_OK:
		# Print UID
		UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
		print ""
		#print "Detected Tag/Card number:", UIDcode
		Loop = 0

	if UIDcode == NaserTag:
		print "Naser's tag detected"

	if UIDcode == NaserCard:
		print "Naser's card detected"

	if UIDcode == AmberTag:
		print "Amber's tag detected"

	if UIDcode == AmberCard:
		print "Amber's card detected"

	if UIDcode == NaserTag or UIDcode == AmberTag or UIDcode == NaserCard or UIDcode == AmberCard:
		if LockStatus == 'Unlocked':
			os.system("sudo python /var/www/code/ServoLock.py")
			LockStatus = 'Locked'
			print "Lock Status:", LockStatus
			time.sleep(1)
			StatusChange = 'Changed'

		elif LockStatus == 'Locked':
			os.system("sudo python /var/www/code/ServoUnlock.py")
			LockStatus = 'Unlocked'
			print "Lock Status:", LockStatus
			if time.localtime().tm_hour >= 17 or time.localtime().tm_hour < 5:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((Host, Port))
				s.sendall('0')         # Send 0 to server for the lights to turn on.
				data = s.recv(1024)
				s.close()
			time.sleep(1)
			StatusChange = 'Changed'

	if StatusChange == 'Changed':

		# Pushbutton LED Status and Buzzer
		if LockStatus == 'Unlocked':
			GPIO.output(11, True)
			time.sleep(.1)
			GPIO.output(11, False)
			time.sleep(.1)
			GPIO.output(11, True)
			time.sleep(.1)
			GPIO.output(11, False)

			GPIO.output(5, False)

		if LockStatus == 'Locked':
			GPIO.output(11, True)
			time.sleep(.1)
			GPIO.output(11, False)
			time.sleep(.1)
			GPIO.output(11, True)
			time.sleep(.1)
			GPIO.output(11, False)
			time.sleep(.1)
			GPIO.output(11, True)
			time.sleep(.1)
			GPIO.output(11, False)

			GPIO.output(5, True)

		# Time to open door and get in/out
		time.sleep(5)

		StatusFile = open('/var/www/code/LockStatus.txt', 'w')
		StatusFile.write(LockStatus)
		StatusFile.close()