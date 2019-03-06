#define S0 6
#define S1 5
#define S2 4
#define S3 3
#define sensorOut 2

int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);

  pinMode(sensorOut, INPUT);

  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);

  redFrequency = pulseIn(sensorOut, LOW);

  Serial.print("R = ");
  Serial.print(redFrequency);
  delay(100);

  digitalWrite(S2, HIGH);
  digitalWrite(S3, HIGH);

  greenFrequency = pulseIn(sensorOut, LOW);

  Serial.print("G = ");
  Serial.print(greenFrequency);
  delay(100);

  digitalWrite(S2, LOW);
  digitalWrite(S3, HIGH);
  
  blueFrequency = pulseIn(sensorOut, LOW);

  Serial.print("B = ");
  Serial.println(blueFrequency);
  delay(100);
}
