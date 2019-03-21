
#include <Arduino.h>
#include <Sensor.h>


Sensor::Sensor(int s0, int s1, int s2, int s3, int out, int enable, int led)
{
    _s0 = s0;
    _s1 = s1;
    _s2 = s2;
    _s3 = s3;
    _out = out;
    _enable = enable;
    _led = led;
}

void Sensor::begin()
{
    pinMode(_s2, OUTPUT);
    pinMode(_s3, OUTPUT);
    pinMode(_enable, OUTPUT);
    pinMode(_led, OUTPUT);
    pinMode(_out, INPUT);

    if(_s0 != -1 && _s1 != -1)
    {
        pinMode(_s0, OUTPUT);
        pinMode(_s1, OUTPUT);

        digitalWrite(_s0, HIGH);
        digitalWrite(_s1, LOW);
    }

    ambient();
}

int Sensor::readR(int pwm)
{
    int val;
    enable(pwm);
    state(_r);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readB(int pwm)
{
    int val;
    enable(pwm);
    state(_b);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readG(int pwm)
{
    int val;
    enable(pwm);
    state(_g);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readK(int pwm)
{
    int val;
    enable(pwm);
    state(_k);
    val = pulseIn(_out,LOW);
    disable();

    if(_gain == 0)
    {
        return val;
    }
    else
    {
        return val * _gain;
    }
}

int Sensor::read(int pwm)
{
  return (readR(pwm) + readG(pwm) + readB(pwm))/3;
}

void Sensor::ambient()
{
    _gain = 0;
    _gain = (readK(0)/3)/100.0;
}

void Sensor::state(int s)
{
    switch(s)
    {
        case 0:
            digitalWrite(_s2, LOW);
            digitalWrite(_s3, LOW);
            break;
        case 1:
            digitalWrite(_s2, LOW);
            digitalWrite(_s3, HIGH);
            break;
        case 2:
            digitalWrite(_s2, HIGH);
            digitalWrite(_s3, LOW);
            break;
        case 3:
            digitalWrite(_s2, HIGH);
            digitalWrite(_s3, HIGH);
            break;
    }
}

void Sensor::LED(int PWM)
{
    if(PWM==255)
    {
        digitalWrite(_led, HIGH);
    }
    else if(PWM==0)
    {
        digitalWrite(_led, LOW);
    }
    else
    {
        analogWrite(_led, PWM);
    }
}

void Sensor::enable(int PWM)
{
    if(_enable != -1)
    {
        digitalWrite(_enable,LOW);
    }

    if(_led != -1)
    {
        LED(PWM);
    }
}

void Sensor::disable()
{
    if(_enable != -1)
    {
        digitalWrite(_enable,HIGH);
    }

    if(_led != -1)
    {
        LED(0);
    }
}
