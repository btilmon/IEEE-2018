//
//#include "Arduino.h"
//#include "Sensor.h"
//
//Sensor::Sensor(int s0, int s1, int out, int enable)
//{
//    _s0 = s0;
//    _s1 = s1;
//    _out = out;
//    _enable = enable;
//
//    const int _red = {"LOW","HIGH"};
//    const int _blue = {"LOW","HIGH"};
//    const int _green = {"LOW","HIGH"};
//    const int _grey = {"LOW","HIGH"};
//}
//
//int Sensor::readR()
//{
//    int val;
//    enable();
//    switch(_red);
//    val = pulsein(out,LOW);
//    disable();
//    return val * _gain;
//}
//
//int Sensor::readB()
//{
//    int val;
//    enable();
//    switch(_blue);
//    val = pulsein(out,LOW);
//    disable();
//    return val * _gain;
//}
//
//int Sensor::readG()
//{
//    int val;
//    enable();
//    switch(_green);
//    val = pulsein(out,LOW);
//    disable();
//    return val * _gain;
//}
//
//int Sensor::readK()
//{
//    int val;
//    enable();
//    switch(_grey);
//    val = pulsein(out,LOW);
//    disable();
//    return val * _gain;
//}
//
//int Sensor::ambient()
//{
//    _gain = (10/readK())/3;
//}
//
//void Sensor::switch(int s[])
//{
//    digitalWrite(_s2, s(0));
//    digitalWrite(_s3, s(1));
//}
//
//void Sensor::enable()
//{
//    if(_enable != -1)
//    {
//        digitalWrite(_enable,LOW);
//    }
//}
//
//void Sensor::disable()
//{
//    if(_enable != -1)
//    {
//        digitalWrite(_enable,HIGH);
//    }
//}
