// Eye Servo 1 - 425 - 575
// Lid Servo 2 - 250 - 400

#include "uart_driver.h"
#include <ax12.h>
#include <BioloidController.h>

#define kNumMotors 2

BioloidController bioloid = BioloidController(1000000);
UARTDriver uart = UARTDriver();

void setup() {
  Serial.begin(57600);
  pinMode(5, OUTPUT);
  digitalWrite(5, HIGH);
}

void loop() {
  uart.listen();
  if (uart.is_acquired()) {

    if (kNumMotors == uart.get_data_length() / 2) {
      uint16_t motor_positions[uart.get_data_length() / 2];
      memcpy(motor_positions, uart.get_data(), uart.get_data_length());
      Serial.print(motor_positions[0]);
      Serial.println();
      Serial.print(motor_positions[1]);
      Serial.println();


    }
    uart.set_acquired(false);
  }
}

void set_motor_positions(uint16_t motor_positions){
  for (int i = 0; i < kNumMotors; i++){

  }
}

void MoveCenter(){
    delay(100);                    // recommended pause
    bioloid.loadPose(Center);   // load the pose from FLASH, into the nextPose buffer
    bioloid.readPose();            // read in current servo positions to the curPose buffer
    Serial.println("###########################");
    Serial.println("Moving servos to centered position");
    Serial.println("###########################");    
    delay(1000);
    bioloid.interpolateSetup(1000); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
    if (RunCheck == 1){
      MenuOptions();
  }
}