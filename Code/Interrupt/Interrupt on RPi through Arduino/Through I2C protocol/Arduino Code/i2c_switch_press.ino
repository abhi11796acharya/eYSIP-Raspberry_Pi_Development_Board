#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int button_state = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(2,INPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  //Wire.onReceive(receiveData);
  Serial.println("Ready!");
}

void loop() {
  // put your main code here, to run repeatedly:
button_state = digitalRead(2);
if (button_state == HIGH){
  Wire.write("1");
}
else{
  Wire.write("1");
}
}
