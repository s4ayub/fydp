// Lid L Servo 1 620 - 780
// Lid R Servo 2 - 250 - 375
// Eye Servo 3 - 420 - 620
// Eyes Up Down Servo 4 - Dead
// Neck Pitch Servo 5 - 440 - 540
// Neck Yaw Servo 6 - 350 - 950

// Left Shoulder Pin 12 - 10-180
// Left Arm Pin 13 - 105-180
// Right Shoulder Pin 14 - 0-180
// Right Arm Pin 15 - 0-75

#include "uart_driver.h"
#include <BioloidController.h>
#include <ax12.h>
#include <Servo.h>

#define BAUD_RATE             57600
#define DYNAMIXEL_BAUD_RATE   1000000

#define COMMAND_MOTORS_HOME       0x01
#define COMMAND_MOTORS_HAPPY      0x02
#define COMMAND_MOTORS_EXCITED    0x03
#define COMMAND_MOTORS_IDLE       0x04

#define NUM_SERVOS            4

#define PIN_LEFT_SHOULDER     12
#define PIN_LEFT_ARM          13
#define PIN_RIGHT_SHOULDER    14
#define PIN_RIGHT_ARM         15

#define NUM_DYNAMIXELS        6

#define DYNAMIXEL_ID_LID_L        1
#define DYNAMIXEL_ID_LID_R        2
#define DYNAMIXEL_ID_EYE_H        3
#define DYNAMIXEL_ID_EYE_V        4
#define DYNAMIXEL_ID_NECK_PITCH   5
#define DYNAMIXEL_ID_NECK_YAW     6

BioloidController bioloid = BioloidController(DYNAMIXEL_BAUD_RATE);
UARTDriver uart = UARTDriver();
Servo left_shoulder;
Servo left_arm;
Servo right_shoulder;
Servo right_arm;
Servo* servos[NUM_SERVOS] = {&left_shoulder, &left_arm, &right_shoulder, &right_arm};

PROGMEM prog_uint16_t dynamixel_start_pos[] = {NUM_DYNAMIXELS, 780, 250, 550, 650, 410, 600};
PROGMEM prog_uint16_t dynamixel_home_pos[] = {NUM_DYNAMIXELS, 700, 300, 520, 650, 510, 650};
PROGMEM prog_uint16_t dynamixel_happy_face_head_up_pos[] = {NUM_DYNAMIXELS, 620, 380, 520, 650, 540, 650};
PROGMEM prog_uint16_t dynamixel_happy_face_head_down_pos[] = {NUM_DYNAMIXELS, 620, 380, 520, 650, 480, 650};
PROGMEM prog_uint16_t dynamixel_left_pos[] = {NUM_DYNAMIXELS, 700, 300, 550, 650, 510, 700};
PROGMEM prog_uint16_t dynamixel_right_pos[] = {NUM_DYNAMIXELS, 700, 300, 490, 650, 510, 600};

int servo_start_pos[] = {90, 150, 90, 30};
int servo_home_pos[] = {180, 105, 0, 75};
int servo_arms_up_pos[] = {0, 105, 180, 75};
int servo_arms_down_pos[] = {0, 180, 180, 0};

void setup() {
  Serial.begin(BAUD_RATE);
  
  for (int i = 0; i < NUM_SERVOS; i++){
    servos[i]->attach(i + PIN_LEFT_SHOULDER);
    servos[i]->write(servo_start_pos[i]);
  }
  delay(1000);
  dynamixel_move(dynamixel_start_pos, 1000);
  motors_move(dynamixel_home_pos, servo_home_pos, 1000);
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
      case COMMAND_MOTORS_EXCITED:
        MoveExcited();
        break;
      case COMMAND_MOTORS_IDLE:
        MoveIdle();
        break;
    }

    uart.set_acquired(false);
  }
}

void motors_move(uint16_t dynamixel_target_pos[], const int servo_target_pos[], int time_ms){
  delay(100);                    // recommended pause
  int frames = (time_ms/BIOLOID_FRAME_LENGTH) + 1;
  float servo_current_pos[NUM_SERVOS];
  float servo_step_size[NUM_SERVOS];
  for (int i = 0; i < NUM_SERVOS; i++){
    servo_current_pos[i] = servos[i]->read();
    servo_step_size[i] = (servo_target_pos[i] - servo_current_pos[i])/frames;
  }
  bioloid.loadPose(dynamixel_target_pos);   // load the pose from FLASH, into the nextPose buffer
  bioloid.readPose();            // read in current servo positions to the curPose buffer
  bioloid.interpolateSetup(time_ms); // setup for interpolation from current->next over 1/2 a second
  while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
      bioloid.interpolateStep();     // move servos, if necessary.
      for (int i = 0; i < NUM_SERVOS; i++){
        servo_current_pos[i] += servo_step_size[i];    
        servos[i]->write(round(servo_current_pos[i]));
      }
      delay(1);
  }
}

void dynamixel_move(uint16_t* pose, int time_ms){
  delay(100);                    // recommended pause
  bioloid.loadPose(pose);   // load the pose from FLASH, into the nextPose buffer
  bioloid.readPose();            // read in current servo positions to the curPose buffer
  bioloid.interpolateSetup(time_ms); // setup for interpolation from current->next over 1/2 a second
  while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
      bioloid.interpolateStep();     // move servos, if necessary. 
      delay(1);
  }
}


void servo_move(const int servo_target_pos[], int num_steps){
  float servo_current_pos[NUM_SERVOS];
  float servo_step_size[NUM_SERVOS];
  for (int i = 0; i < NUM_SERVOS; i++){
    servo_current_pos[i] = servos[i]->read();
    servo_step_size[i] = (servo_target_pos[i] - servo_current_pos[i])/num_steps;
  }

  for (int n = 0; n < num_steps; n++){
    for (int i = 0; i < NUM_SERVOS; i++){
      servo_current_pos[i] += servo_step_size[i];    
      servos[i]->write(round(servo_current_pos[i]));
    }
  }
}


void MoveHome() {
  motors_move(dynamixel_home_pos, servo_home_pos, 1000);
}

void MoveHappy(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 800);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 300);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 300);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 300);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 300);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 300);
}

void MoveExcited(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_up_pos, 800);
  motors_move(dynamixel_happy_face_head_down_pos, servo_home_pos, 400);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_up_pos, 400);
  motors_move(dynamixel_happy_face_head_down_pos, servo_home_pos, 400);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_up_pos, 400);
  motors_move(dynamixel_happy_face_head_down_pos, servo_home_pos, 400);
}

void MoveIdle(){
  motors_move(dynamixel_left_pos, servo_home_pos, 800);
  motors_move(dynamixel_right_pos, servo_home_pos, 300);
  motors_move(dynamixel_left_pos, servo_home_pos, 300);
  motors_move(dynamixel_right_pos, servo_home_pos, 300);
}