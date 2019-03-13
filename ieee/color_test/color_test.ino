#include <string.h>

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

int aRedFrequency = 0;
int aGreenFrequency = 0;
int aBlueFrequency = 0;
int aOut = 0;

int bRedFrequency = 0;
int bGreenFrequency = 0;
int bBlueFrequency = 0;
int bOut = 0;

int scale = 1;

void setup() {
  // put your setup code here, to run once:
  pinMode(aS0, OUTPUT);
  pinMode(aS1, OUTPUT);
  pinMode(aS2, OUTPUT);
  pinMode(aS3, OUTPUT);

  pinMode(bS0, OUTPUT);
  pinMode(bS1, OUTPUT);
  pinMode(bS2, OUTPUT);
  pinMode(bS3, OUTPUT);
  
  pinMode(enable, OUTPUT);
  
  pinMode(aSensorOut, INPUT);
  pinMode(bSensorOut, INPUT);
  
  digitalWrite(aS0, HIGH);
  digitalWrite(aS1, LOW);

  digitalWrite(bS0, HIGH);
  digitalWrite(bS1, LOW);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  //enable pin
  digitalWrite(enable, LOW);
  
  digitalWrite(aS2, LOW);
  digitalWrite(aS3, LOW);

  digitalWrite(bS2, LOW);
  digitalWrite(bS3, LOW);

  aRedFrequency = pulseIn(aSensorOut, LOW);
  bRedFrequency = pulseIn(bSensorOut, LOW);
  

  //Serial.print("R = ");
  //Serial.print(redFrequency);
  //delay(100);

  digitalWrite(aS2, HIGH);
  digitalWrite(aS3, HIGH);

  digitalWrite(bS2, HIGH);
  digitalWrite(bS3, HIGH);

  aGreenFrequency = pulseIn(aSensorOut, LOW);
  bGreenFrequency = pulseIn(bSensorOut, LOW);
  //Serial.print("G = ");
  //Serial.print(greenFrequency);
  //delay(100);

  digitalWrite(aS2, LOW);
  digitalWrite(aS3, HIGH);

  digitalWrite(bS2, LOW);
  digitalWrite(bS3, HIGH);
  
  aBlueFrequency = pulseIn(aSensorOut, LOW);
  bBlueFrequency = pulseIn(bSensorOut, LOW);

  //Serial.print("B = ");
  //Serial.println(blueFrequency);
  //delay(100);


  aRedFrequency = aRedFrequency * scale;
  aBlueFrequency = aBlueFrequency * scale;
  aGreenFrequency = aGreenFrequency * scale;

  bRedFrequency = bRedFrequency * scale;
  bBlueFrequency = bBlueFrequency * scale;
  bGreenFrequency = bGreenFrequency * scale;

  
  
//  aOut = (aRedFrequency + aBlueFrequency + aGreenFrequency)/3;
//  bOut = (bRedFrequency + bBlueFrequency + bGreenFrequency)/3;
//  Serial.println(color_processing(aRedFrequency,aGreenFrequency,aBlueFrequency) + "^" + color_processing(bRedFrequency,bGreenFrequency,bBlueFrequency));
  Serial.println(color_processing(aRedFrequency,aGreenFrequency,aBlueFrequency) + "^" + String(aRedFrequency) + "^" + String(aGreenFrequency) + "^" + String(aBlueFrequency));
  
//  Serial.println(aRedFrequency);
  
}

String color_processing(int r, int g, int b)
{

  if ((r < 80) and (g < 80) and (b < 80))
  {
    return "w";
  }

  else if ((r < 120) and (g > 150) and (b > 200))
  {
    return "r";
  }

  else if ((r > 230) and (b < 100) and (g > 120 ))
  {
    return "b";
  }
   
  else if ((r > 175) and (g < 120) and (b > 190 ))
  {
    return "g";
  }

  else if ((r < 90) and (b < 170) and (g < 120 ))
  {
    return "y";
  }

  else
  {
    return "x";
  }
}
