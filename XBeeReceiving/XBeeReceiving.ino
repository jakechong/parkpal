/*
   Software Serial Exercise

   Receives from the hardware serial, sends to software serial.
   Receives from software serial, sends to hardware serial.
 
   The circuit: 
   * RX is digital pin 10 (connect to TX of other device)
   * TX is digital pin 11 (connect to RX of other device)
   
   Note:
   Not all pins on the Mega and Mega 2560 support change interrupts, 
   so only the following can be used for RX: 
   10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69
   
   Not all pins on the Leonardo support change interrupts, 
   so only the following can be used for RX: 
   8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI).
 
   Reference Page: http://arduino.cc/en/Reference/Serial

   created November 2013
   by Eric Burger
   based on Tom Igoe's SoftwareSerialExample
   which is based on Mikal Hart's example
   
   This example code is in the public domain.
*/

#include <SoftwareSerial.h>
int i = 0;
SoftwareSerial myXBee(10, 11); // RX=>DOUT, TX=>DIN


void setup(){
  Serial.begin(9600); 
  while (!Serial) {;}
  myXBee.begin(9600);
}

void loop(){
  // Check software serial port
  while( myXBee.available() > 0 ){
    i = myXBee.read();
    Serial.write(i);
  }
  // A delay is not necessary, but 
  // does not hurt either.
  delay(1000);
}
