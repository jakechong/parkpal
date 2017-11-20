#define trigPin1 10
#define trigPin2 9
#define echoPin1 13
#define echoPin2 8
#include <SoftwareSerial.h>

SoftwareSerial myXBee(11,12);

void setup() {
  Serial.begin (9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(echoPin2, INPUT);
  while (!Serial) {;}
  myXBee.begin(9600);
}

void loop() {
  byte yesCar1, yesCar2;
  
  float duration1, distance1;
  digitalWrite(trigPin1, LOW); 
  delayMicroseconds(2);
 
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  
  duration1 = pulseIn(echoPin1, HIGH);
  distance1 = (duration1 / 2) * 0.0344;

  float duration2, distance2;
  digitalWrite(trigPin2, LOW); 
  delayMicroseconds(2);
 
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  
  duration2 = pulseIn(echoPin2, HIGH);
  distance2 = (duration2 / 2) * 0.0344;
  
  if (distance1 >= 80 || distance1 <= 5){
    yesCar1 = 1;
  }
  else {
    yesCar1 = 0;
  }
  if (distance2 >= 80 || distance2 <= 5){
    yesCar2 = 1;
  }
  else {
    yesCar2 = 0;
  }
  myXBee.println(yesCar1);
  myXBee.println(yesCar2);
  delay(10000);
}
