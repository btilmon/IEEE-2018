
#include <Sensor.h>

#define aryOE 4
#define aryLED 5
#define aryS2 2
#define aryS3 3

#define tpeOE 46
#define tpeLED 44
#define tpeS2 52
#define tpeS3 50
#define tpeOUT 48

//Gain scale value
#define constG 7

int aryO[5] = {8,9,10,11,12};

Sensor ary[5];
Sensor tape(-1,-1,tpeS2,tpeS3,tpeOUT,tpeOE,tpeLED);

void setup() 
{ 
  Serial.begin(9600);
  pinMode(aryOE, OUTPUT);
  pinMode(aryLED, OUTPUT);

  digitalWrite(aryOE, LOW);
  digitalWrite(aryLED, HIGH);

  tape.constant = constG;
  tape.begin();
  
  for(int i = 0; i<5; i++)
  {
    ary[i].constant = constG;
    ary[i].begin(aryS2,aryS3,aryO[i]);
  }
}

void loop() 
{
  String out = "";

  for(int i = 0; i<5; i++)
  {
    out = out + "[" + String(ary[i].getGain()) + "^" + String(ary[i].read()) + "]^";
  }

  Serial.println(out + "[" + String(tape.getGain()) + "^" + String(tape.read())) + "]";
  
}
