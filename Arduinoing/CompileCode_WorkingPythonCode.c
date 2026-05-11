#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <Servo.h>
 
MPU6050 mpu;
Servo Servo1;
Servo Servo2;
 
 
 
int const INTERRUPT_PIN = 2;
 
int SERVO_PIN_1 = 9;
int SERVO_PIN_2 = 10;
 
int MOTOR_PIN_P_1 = 11;
int MOTOR_PIN_P_2 = 6;
int MOTOR_PIN_Q_1 = 5;
int MOTOR_PIN_Q_2 = 3;
bool blinkState;
 
/* MPU vars */
bool DMPReady = false;
uint8_t devStatus;
uint16_t packetSize;
uint8_t FIFOBuffer[64];
 
Quaternion q;
VectorFloat gravity;
float ypr[3];
 
volatile bool MPUInterrupt = false;
void DMPDataReady() {
  MPUInterrupt = true;
}
 
void setup() {
  Wire.begin();
  Wire.setClock(400000);
 
  Serial.begin(115200);
  while (!Serial);
 
  Servo1.attach(SERVO_PIN_1);
  Servo2.attach(SERVO_PIN_2);
 
  mpu.initialize();
 
  pinMode(INTERRUPT_PIN, INPUT);
 
  pinMode(MOTOR_PIN_P_1, OUTPUT);
  pinMode(MOTOR_PIN_P_2, OUTPUT);
  pinMode(MOTOR_PIN_Q_1, OUTPUT);
  pinMode(MOTOR_PIN_Q_2, OUTPUT);
 
  if (!mpu.testConnection()) {
    while (true);
  }
 
  // Wait for Python to start
  while (!Serial.available());
  while (Serial.available()) Serial.read();
 
  devStatus = mpu.dmpInitialize();
 
  mpu.setXGyroOffset(0);
  mpu.setYGyroOffset(0);
  mpu.setZGyroOffset(0);
 
  if (devStatus == 0) {
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
 
    mpu.setDMPEnabled(true);
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), DMPDataReady, RISING);
 
    DMPReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
  }
 
  pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop() {
  if (!DMPReady) return;
 
  //  Read sensor and send to Python
  if (mpu.dmpGetCurrentFIFOPacket(FIFOBuffer)) {
    mpu.dmpGetQuaternion(&q, FIFOBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
 
    float yaw_deg = ypr[0] * 180 / M_PI;
 
    Serial.print("S:");
    Serial.println(yaw_deg);
 
    blinkState = !blinkState;
    digitalWrite(LED_BUILTIN, blinkState);
  }
 
  //  Read command from Python
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
 
    if (cmd.startsWith("C:")) {
      int angle = cmd.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      Servo1.write(angle);
    }
    if (cmd.startsWith("A:")) {
      int angle = cmd.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      Servo1.write(angle);
    }
    if (cmd.startsWith("B:")) {
      int angle = cmd.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      Servo2.write(angle);
    }
    if (cmd.startsWith("D:")) {
      int PWM_1 = cmd.substring(2).toInt();
      PWM_1 = constrain(PWM_1, 0, 100);
      analogWrite(MOTOR_PIN_P_1, (int)(PWM_1 / 100.0 * 255)); // analogWrite needs a value between 0 and 255
      analogWrite(MOTOR_PIN_Q_1, (int)(PWM_1 / 100.0 * 255));
    }
    if (cmd.startsWith("E:")) {
      int PWM_2 = cmd.substring(2).toInt();
      PWM_2 = constrain(PWM_2, 0, 100);
      analogWrite(MOTOR_PIN_P_2, (int)(PWM_2 / 100.0 * 255));
      analogWrite(MOTOR_PIN_Q_2, (int)(PWM_2 / 100.0 * 255));
    }
  }
}