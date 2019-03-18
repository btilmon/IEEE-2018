#include <string.h>
#include <Sensor.h>

#define aS0 53
#define aS1 51
#define aS2 49
#define aS3 47
#define aSensorOut 45

#define bS0 37
#define bS1 35
#define bS2 33
#define bS3 31
#define bSensorOut 29
#define enable 23

//Make instance of sensor class with hardware addresses
//-1 means this pin is not used
Sensor sense1(aS2,aS3,aSensorOut,-1);
Sensor sense2(bS2,bS3,bSensorOut,enable);

//int scale = 10;

void setup() {
  // put your setup code here, to run once:

  // These pins are currently controlled by arduino
  // will be re-done to use DIP switches or jumpers
  pinMode(aS0, OUTPUT);
  pinMode(aS1, OUTPUT);
  digitalWrite(aS0, HIGH);
  digitalWrite(aS1, LOW);
  pinMode(bS0, OUTPUT);
  pinMode(bS1, OUTPUT);
  digitalWrite(bS0, HIGH);
  digitalWrite(bS1, LOW);

  //Normal setup

  //Mesure ambient light, and calculate a gain value for output values
  sense1.ambient();
  sense2.ambient();

  Serial.begin(9600);
}

void loop() 
{
  // put your main code here, to run repeatedly:

  // The Sensor class returns the raw data from the Arduino.pulseIn method multiplied by a gain value calculated with the Sensor.ambient method.
  // Arduino.pulseIn returns PWM pulse length in micro seconds.

  Serial.println(tapeColor(grayscale(sense1.readR(), sense1.readG(), sense1.readB())) + "^" + blockColor(grayscale(sense2.readR(), sense2.readG(), sense2.readB())));
  Serial.println(grayscale(sense1.readR(), sense1.readG(), sense1.readB()));
}

int grayscale(int r,int g,int b)
{
  int scale = 10;

  return (r*scale + g*scale + b*scale)/3;
}

String tapeColor(int g)
{
  if(g > 2000)
  {
    return "x";
  }

  else
  {
    return "c";
  }

//
//  if(g < 900 and g > 800)
//  {
//    return "y";
//  }
//  
//  else if(g > 2900)
//  {
//    return "r";
//  }
//
//  else if(g > 1600 and g < 1700)
//  {
//    return "b";
//  }
//
//  else if(g > 1230 and g < 1320)
//  {
//    return "g";
//  }
//  
//  else if(g > 500 and g < 800)
//  {
//    return "w";
//  }
//  
//  else
//  {
//    return "x";
//  }
}

String blockColor(int g)
{
//  if((r < 55) and (g > 80) and (b < 85))
//  {
//    return "r";
//  }
//
//  else if((r < 50) and (g < 80) and (b < 80))
//  {
//    return "y";
//  }
//
//  else if((r > 75) and (g > 100) and (b > 90))
//  {
//    return "b";
//  }
//
//  else if((r < 75) and (g < 100) and (b < 100))
//  {
//    return "g";
//  }
//
//  else
//  {
//    return "x";
//  }

  if(g < 650)
  {
    return "y";
  }
  
  else if(g > 1180 and g < 1210)
  {
    return "r";
  }

  else if(g > 880 and g < 940)
  {
    return "b";
  }

  else if(g > 1230 and g < 1280)
  {
    return "g";
  }
  else
  {
    return "x";
  }
}
