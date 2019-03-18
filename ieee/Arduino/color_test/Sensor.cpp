
#include "Arduino.h"
#include "Sensor.h"

Sensor::Sensor(int s2, int s3, int out, int enable)
{
    _s2 = s2;
    _s3 = s3;
    _out = out;
    _enable = enable;

    pinMode(_s2, OUTPUT);
    pinMode(_s3, OUTPUT);
    pinMode(_enable, OUTPUT);
    pinMode(_out, INPUT);
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

int Sensor::ambient()
{
    _gain = 0;
    _gain = (10/readK())/3;
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