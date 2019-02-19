import pigpio

class LDRPWM():

    def __init__(self,pin):
        self.PWM = pin
        self.pi = pigpio.pi()

    def Spin(self,speed):
        self.pi.set_PWM_dutycycle(self.PWM,speed)
