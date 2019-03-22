#include <NewPing.h>
#include <string.h>
#define trig1 52
#define echo1 53
#define trig2 50
#define echo2 51
#define trig3 48
#define echo3 49

#define maxD 10000

int r1 = 0;

NewPing sonar1(trig1, echo1, maxD);
NewPing sonar2(trig2, echo2, maxD);
NewPing sonar3(trig3, echo3, maxD);

void setup() {
  Serial.begin(57600);
}


void loop() {
  
  
  Serial.println(String(int(sonar1.ping_cm()*10)) + "^" + String(int(sonar2.ping_cm()*10)) + "^" + String(int(sonar3.ping_cm()*10)));

}
