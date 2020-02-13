// Eye Servo 1 - 425 - 575
// Lid Servo 2 - 250 - 400

#include "uart_driver.h"
#include <BioloidController.h>
#include <ax12.h>
#include <Servo.h>

#define BAUD_RATE             57600

#define COMMAND_MOTORS_HOME   0x01
#define COMMAND_MOTORS_HAPPY  0x02

#define PIN_LEFT_ARM          3
#define PIN_RIGHT_ARM         4

#define SERVO_LEFT_CENTER     90
#define SERVO_RIGHT_CENTER    90

#define DYNAMIXEL_ID_EYES     1
#define DYANMIXEL_ID_LID      2
#define DYNAMIXEL_CENTER_EYES 500
#define DYNAMIXEL_CENTER_LID  325

PROGMEM prog_uint16_t dynamixel_center[] = {2, DYNAMIXEL_CENTER_EYES, DYNAMIXEL_CENTER_LID};
PROGMEM prog_uint16_t look_left[] = {2, 450, 275};
PROGMEM prog_uint16_t look_right[] = {2, 550, 375};

BioloidController bioloid = BioloidController(1000000);
Servo left_arm;
Servo right_arm;
UARTDriver uart = UARTDriver();

void setup() {
  Serial.begin(BAUD_RATE);

  pinMode(5, OUTPUT);
  digitalWrite(5, HIGH);

  left_arm.attach(PIN_LEFT_ARM);
  right_arm.attach(PIN_RIGHT_ARM);
  left_arm.write(0);
  right_arm.write(0);
}

void loop() {
  uart.listen();
  if (uart.is_acquired()) {

    switch(uart.get_command_code()){
      case COMMAND_MOTORS_HOME:
        MoveHome();
        break;
      case COMMAND_MOTORS_HAPPY:
        MoveHappy();
        break;
    }

    uart.set_acquired(false);
  }
}

void pose_step(uint16_t* pose, int time_ms){
  delay(100);                    // recommended pause
  bioloid.loadPose(pose);   // load the pose from FLASH, into the nextPose buffer
  bioloid.readPose();            // read in current servo positions to the curPose buffer
  delay(1000);
  bioloid.interpolateSetup(time_ms); // setup for interpolation from current->next over 1/2 a second
  while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
      bioloid.interpolateStep();     // move servos, if necessary. 
      delay(1);
  }
}

void 

void MoveHome() {

  step_from_current(dynamixel_center, 1000);
  left_arm.write(SERVO_LEFT_CENTER);
  right_arm.write(SERVO_RIGHT_CENTER);

}

void MoveHappy(){
  step_from_current(look_left, 500);
  step_from_current(look_right, 500);
  left_arm.write(120);
  right_arm.write(120);
}