#include <string.h>
#include <Sensor.h>


#define aS2 49
#define aS3 47
#define aSensorOut 45

#define bS2 33
#define bS3 31
#define bSensorOut 29
#define enable 23

//Make instance of sensor class with hardware addresses
//-1 means this pin is not used
Sensor sense1;
Sensor sense2;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:

  sense1.begin(aS2,aS3,aSensorOut,-1);
  sense2.begin(bS2,bS3,bSensorOut,enable);
  sense1.ambient();
  sense2.ambient();
}

void loop() 
{
  // put your main code here, to run repeatedly:

  Serial.println(tapeColor(sense1.read()) + "^" + blockColor(sense1.read()));
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
