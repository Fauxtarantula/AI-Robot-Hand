//Just a prototype
//#include <SoftwareSerial.h>
#include <Servo.h>
#include<TimerOne.h>
#define LEDpin 6

Servo index,middle;
String a,binary;
int x, i, state, test;
int fgType = 1;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  index.attach(4);
  middle.attach(5);
  index.write(0);
  middle.write(0);
}

void loop() {
  if (Serial.available()>0){
    a=Serial.readString();
    //Serial.println(readBinary(a));
    //Serial.print(a);
    readBinary(a);
    }
}
void readBinary(String bin){ //Should prob save in array
  for(i = 0; i<bin.length()-1;i++){
    binary = bin.charAt(i);
    //state += binary.toInt();
    
  }
}
