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

#define BAUD_RATE                       57600
#define DYNAMIXEL_BAUD_RATE             1000000

#define COMMAND_MOVE_HOME               0x01
#define COMMAND_MOVE_HAPPY              0x02
#define COMMAND_MOVE_EXCITED            0x03
#define COMMAND_MOVE_IDLE               0x04
#define COMMAND_MOVE_WAVE_HELLO         0x05
#define COMMAND_MOVE_HUG                0x06
#define COMMAND_MOVE_WOAH               0x07
#define COMMAND_MOVE_FORTNITE_DANCE     0x08
#define COMMAND_RESET_TORQUE_ENABLE     0xaa

#define NUM_SERVOS                      4

#define PIN_LEFT_SHOULDER               12
#define PIN_LEFT_ARM                    13
#define PIN_RIGHT_SHOULDER              14
#define PIN_RIGHT_ARM                   15

#define NUM_DYNAMIXELS                  6

#define DYNAMIXEL_ID_LID_L              1
#define DYNAMIXEL_ID_LID_R              2
#define DYNAMIXEL_ID_EYE_H              3
#define DYNAMIXEL_ID_EYE_V              4
#define DYNAMIXEL_ID_NECK_PITCH         5
#define DYNAMIXEL_ID_NECK_YAW           6

#define SMOOTHSTEP(x)                   ((x) * (x) * (3 - 2 * (x)))

BioloidController bioloid = BioloidController(DYNAMIXEL_BAUD_RATE);
UARTDriver uart = UARTDriver();
Servo left_shoulder;
Servo left_arm;
Servo right_shoulder;
Servo right_arm;
Servo* servos[NUM_SERVOS] = {&left_shoulder, &left_arm, &right_shoulder, &right_arm};

PROGMEM prog_uint16_t dynamixel_start_pos[] = {NUM_DYNAMIXELS, 780, 250, 550, 650, 460, 600};
PROGMEM prog_uint16_t dynamixel_home_pos[] = {NUM_DYNAMIXELS, 700, 300, 520, 650, 510, 650};
PROGMEM prog_uint16_t dynamixel_happy_face_head_up_pos[] = {NUM_DYNAMIXELS, 620, 380, 520, 650, 535, 650};
PROGMEM prog_uint16_t dynamixel_happy_face_head_down_pos[] = {NUM_DYNAMIXELS, 620, 380, 520, 650, 480, 650};
PROGMEM prog_uint16_t dynamixel_left_pos[] = {NUM_DYNAMIXELS, 700, 300, 550, 650, 510, 680};
PROGMEM prog_uint16_t dynamixel_right_pos[] = {NUM_DYNAMIXELS, 700, 300, 490, 650, 510, 620};

int servo_start_pos[] = {90, 150, 90, 30};
int servo_home_pos[] = {180, 105, 0, 75};
int servo_arms_up_pos[] = {0, 105, 180, 75};
int servo_arms_down_pos[] = {0, 180, 180, 0};
int servo_arms_sway_up_pos[] = {160, 120, 20, 60};
int servo_arms_left_wave_up_pos[] = {0, 105, 0, 75};
int servo_arms_left_wave_down_pos[] = {0, 180, 0, 70};
int servo_arms_right_wave_up_pos[] = {180, 105, 180, 75};
int servo_arms_right_wave_down_pos[] = {180, 100, 180, 0};
int servo_arms_right_wave_fwd_pos[] = {130, 105, 130, 75};
int servo_arms_hug_close[] = {90, 105, 90, 75};
int servo_arms_hug_open[] = {90, 180, 90, 0};
int servo_arms_left_up_right_down[] = {45, 105, 45, 75};
int servo_arms_left_down_right_up[] = {135, 105, 135, 75};

void setup() {
  Serial.begin(BAUD_RATE);
  ax12SetRegister2(5, AX_TORQUE_LIMIT_L, 1023); 
  Relax(5);

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
    // Needed to ensure motor 5 does not turn off from ALARM SHUTODWN
    ax12SetRegister2(5, AX_TORQUE_LIMIT_L, 1023); 
    Relax(5);
    switch(uart.get_command_code()){
      case COMMAND_MOVE_HOME:
        MoveHome();
        break;
      case COMMAND_MOVE_HAPPY:
        MoveHappy();
        break;
      case COMMAND_MOVE_EXCITED:
        MoveExcited();
        break;
      case COMMAND_MOVE_IDLE:
        MoveIdle();
        break;
      case COMMAND_MOVE_WAVE_HELLO:
        MoveWaveHello();
        break;
      case COMMAND_MOVE_HUG:
        MoveHug();
        break;
      case COMMAND_MOVE_WOAH:
        MoveWoah();
        break;
      case COMMAND_MOVE_FORTNITE_DANCE:
        MoveFortniteDance();
        break;
      case COMMAND_RESET_TORQUE_ENABLE:
        ResetTorqueEnable();
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
  // delay(100);                    // recommended pause
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

void servo_smoothstep(const int servo_target_pos[], int num_steps){
  float servo_current_pos[NUM_SERVOS];
  for (int i = 0; i < NUM_SERVOS; i++){
    servo_current_pos[i] = servos[i]->read();
  }

  for (int n = 0; n < num_steps; n++){
    for (int i = 0; i < NUM_SERVOS; i++){
      float v = float(n) / float(num_steps);      // Iteration divided by the number of steps.
      v = SMOOTHSTEP(v);            // Run the smoothstep expression on v.
      float pos = (servo_target_pos[i] * v) + (servo_current_pos[i] * (1 - v));   // Run the linear interpolation expression using the current smoothstep result.
      servos[i]->write(round(pos));
    }
  }
}

void MoveHome() {
  motors_move(dynamixel_home_pos, servo_home_pos, 1000);
}

void MoveHappy(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 800);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 400);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 400);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 400);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_down_pos, 400);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_up_pos, 400);
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
  motors_move(dynamixel_right_pos, servo_arms_sway_up_pos, 800);
  servo_smoothstep(servo_home_pos, 600);
  servo_smoothstep(servo_arms_sway_up_pos, 1000);
  motors_move(dynamixel_left_pos, servo_home_pos, 800);
  motors_move(dynamixel_right_pos, servo_home_pos, 800);
  servo_smoothstep(servo_arms_sway_up_pos, 800);
  servo_smoothstep(servo_home_pos, 500);
}

void MoveWaveHello(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_left_wave_up_pos, 800);
  servo_smoothstep(servo_arms_left_wave_down_pos, 500);
  servo_smoothstep(servo_arms_left_wave_up_pos, 500);
  servo_smoothstep(servo_arms_left_wave_down_pos, 500);
  servo_smoothstep(servo_arms_left_wave_up_pos, 500);
}

void MoveHug(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_hug_open, 800);
  servo_smoothstep(servo_arms_hug_close, 1000);
}

void MoveWoah(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_left_wave_down_pos, 1000);
  servo_smoothstep(servo_arms_left_wave_up_pos, 400);
  servo_smoothstep(servo_arms_left_wave_down_pos, 900);
  delay(1250);
  servo_smoothstep(servo_arms_hug_close, 700);
  servo_smoothstep(servo_arms_left_up_right_down, 600);
  motors_move(dynamixel_left_pos, servo_arms_hug_open, 450);
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_left_down_right_up, 300);
  servo_smoothstep(servo_arms_hug_close, 200);
  servo_smoothstep((int[]){90, 105, 90, 75}, 200);
  servo_smoothstep((int[]){80, 115, 100, 65}, 200);
  servo_smoothstep((int[]){90, 105, 90, 75}, 200);
  servo_smoothstep((int[]){100, 115, 80, 65}, 200);
}

void MoveFortniteDance(){
  motors_move(dynamixel_happy_face_head_up_pos, servo_arms_right_wave_up_pos, 500);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_right_wave_fwd_pos, 100);
  motors_move(dynamixel_happy_face_head_up_pos,servo_arms_right_wave_up_pos, 100);
  motors_move(dynamixel_happy_face_head_down_pos, servo_arms_right_wave_fwd_pos, 100);
  for (int i = 0; i < 10; i++){
    motors_move(dynamixel_happy_face_head_up_pos, servo_arms_right_wave_up_pos, 100);
    motors_move(dynamixel_happy_face_head_down_pos, servo_arms_right_wave_fwd_pos, 100);
  }
}

void ResetTorqueEnable(){
  TorqueOn(5);
  ax12SetRegister2(5, AX_TORQUE_LIMIT_L, 1023);
  motors_move(dynamixel_happy_face_head_up_pos, servo_home_pos, 500);
  motors_move(dynamixel_happy_face_head_down_pos, servo_home_pos, 500);
}