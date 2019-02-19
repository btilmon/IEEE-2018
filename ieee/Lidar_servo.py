#import RPi.GPIO as GPIO
#import time
import pigpio

#try:
pi1 = pigpio.pi()
ldrPWM= 17
pi1.set_PWM_dutycycle(ldrPWM,0)
#pi1.write(17,0)
#except:
#    pi.set_PWM_dutycycle(servoPIN,0)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)
#
#p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
#p.start(2.5) # Initialization
#try:
#  while True:
#    p.ChangeDutyCycle(5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(7.5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(10)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(12.5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(10)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(7.5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(5)
#    time.sleep(0.5)
#    p.ChangeDutyCycle(2.5)
#    time.sleep(0.5)
#except KeyboardInterrupt:
#  p.stop()
#  GPIO.cleanup()