
#ifndef H_Sensor
#define H_Sensor

#include <Arduino.h>


class Sensor
{
    public:
        Sensor(int s0, int s1, int s2, int s3, int out, int enable, int led);
        Sensor(int s2, int s3, int Out);
        Sensor();
        void begin();
        void ambient();
        void begin(int s2, int s3, int Out);
        void setLED(int pwm);
        int read();
        int readR();
        int readG();
        int readB();
        int readK();
        float getGain();
        float constant;
    private:
        void state(int s);
        void enable();
        void disable();
        int _s0;
        int _s1;
        int _s2;
        int _s3;
        int _out;
        int _enable;
        int _led;
        float _gain;

        const int _r = 0;
        const int _b = 1;
        const int _k = 2;
        const int _g = 3;
};

#endif
