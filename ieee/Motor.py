import pigpio

class Motor():

    def __init__(self, direction, PWM):
        self.inv = False
        self.pi = pigpio.pi()
        self.dir = direction
        self.pi.set_mode(self.dir, pigpio.OUTPUT)
        self.pwm = PWM

    def Inverse(self):
        self.inv = not self.inv

    def Drive(self, direction, PWM):
        self.Stop()
        if self.inv:
            if direction==1:
                self.pi.write(self.dir,0)
            else:
                self.pi.write(self.dir,1)
        else:
            self.pi.write(self.dir,direction)

        self.pi.set_PWM_dutycycle(self.pwm,PWM)

    def Stop(self):
        self.pi.set_PWM_dutycycle(self.pwm,0)
        self.pi.write(self.dir,0)
