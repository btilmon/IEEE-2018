#include <string.h>

#define aS0 45
#define aS1 47
#define aS2 49
#define aS3 53
#define aSensorOut 51

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

  Serial.begin(57600);
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
  
  aOut = (aRedFrequency + aBlueFrequency + aGreenFrequency)/3;
  bOut = (bRedFrequency + bBlueFrequency + bGreenFrequency)/3;
  Serial.println(String(aOut) + "^" + String(bOut));
  
}
