import pigpio

class Motor():

    def __init__(self, in1, in2, PWM):
        self.inv = False
        self.pi = pigpio.pi()
        self.i1 = in1
        self.i2 = in2
        self.pi.set_mode(self.i1, pigpio.OUTPUT)
        self.pi.set_mode(self.i2, pigpio.OUTPUT)
        self.pwm = PWM

    def Inverse(self):
        self.inv = not self.inv

    def Drive(self, direction, PWM):
        self.Stop()
        if self.inv:
            if direction==1:
                self.pi.write(self.i1,0)
                self.pi.write(self.i2,1)
            else:
                self.pi.write(self.i1,1)
                self.pi.write(self.i2,0)
        else:
            if direction==1:
                self.pi.write(self.i1,1)
                self.pi.write(self.i2,0)
            else:
                self.pi.write(self.i1,0)
                self.pi.write(self.i2,1)

        self.pi.set_PWM_dutycycle(self.pwm,PWM)

    def Stop(self):
        self.pi.set_PWM_dutycycle(self.pwm,0)
        self.pi.write(self.i1,0)
        self.pi.write(self.i2,0)
