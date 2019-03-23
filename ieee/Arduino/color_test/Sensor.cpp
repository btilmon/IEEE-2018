
#include <Arduino.h>
#include <Sensor.h>


Sensor::Sensor()
{

}

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

Sensor::Sensor(int s2, int s3, int out)
{
    _s0 = -1;
    _s1 = -1;
    _s2 = s2;
    _s3 = s3;
    _out = out;
    _enable = -1;
    _led = -1;
}

void Sensor::begin()
{
    pinMode(_s2, OUTPUT);
    pinMode(_s3, OUTPUT);
    pinMode(_out, INPUT);

    if(_led != -1)
    {
        pinMode(_led, OUTPUT);
        setLED(255);
    }

    if(_enable != -1)
    {
        pinMode(_enable, OUTPUT);
    }

    if(_s0 != -1 && _s1 != -1)
    {
        pinMode(_s0, OUTPUT);
        pinMode(_s1, OUTPUT);

        digitalWrite(_s0, HIGH);
        digitalWrite(_s1, LOW);
    }

    ambient();
}

void Sensor::begin(int s2, int s3, int out)
{
    _s0 = -1;
    _s1 = -1;
    _s2 = s2;
    _s3 = s3;
    _out = out;
    _enable = -1;
    _led = -1;

    pinMode(_s2, OUTPUT);
    pinMode(_s3, OUTPUT);
    pinMode(_out, INPUT);

    ambient();
}

float Sensor::getGain()
{
    return _gain;
}

int Sensor::readR()
{
    int val;
    enable();
    state(_r);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readB()
{
    int val;
    enable();
    state(_b);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readG()
{
    int val;
    enable();
    state(_g);
    val = pulseIn(_out,LOW);
    disable();
    return val * _gain;
}

int Sensor::readK()
{
    int val;
    enable();
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

int Sensor::read()
{
  return (readR() + readG() + readB())/3;
}

void Sensor::ambient()
{
    _gain = 0;
    _gain = ((readK()*constant)/3)/100.0;
}

void Sensor::state(int s)
{
    if(_s2 != -1 && _s3 != -1)
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
}

void Sensor::setLED(int pwm)
{
    if(pwm==255)
    {
        digitalWrite(_led, HIGH);
    }
    else if(PWM==0)
    {
        digitalWrite(_led, LOW);
    }
    else
    {
        analogWrite(_led, pwm);
    }
}

void Sensor::enable()
{
    if(_enable != -1)
    {
        digitalWrite(_enable,LOW);
    }
}

void Sensor::disable()
{
    if(_enable != -1)
    {
        digitalWrite(_enable,HIGH);
    }
}
