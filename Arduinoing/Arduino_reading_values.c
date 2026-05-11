#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include "Wire.h"
#endif

MPU6050 mpu;

const int INTERRUPT_PIN = 2;

bool dmpReady = false;
uint8_t devStatus;
uint16_t packetSize;
uint8_t fifoBuffer[64];

Quaternion q;
VectorFloat gravity;
float ypr[3];

volatile bool mpuInterrupt = false;

void dmpDataReady() {
  mpuInterrupt = true;
}

void setup() {
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
    Wire.setClock(400000);
  #endif

  Serial.begin(115200);
  while (!Serial) {
    // Wait for serial connection on boards that need it.
    // On Arduino Nano this usually continues immediately.
  }

  pinMode(INTERRUPT_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("Initializing MPU6050...");
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed.");
    while (true) {
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
      delay(200);
    }
  }

  Serial.println("MPU6050 connected.");
  Serial.println("Initializing DMP...");

  devStatus = mpu.dmpInitialize();

  // These offsets are placeholders.
  // For better accuracy, replace them with calibrated values later.
  mpu.setXGyroOffset(0);
  mpu.setYGyroOffset(0);
  mpu.setZGyroOffset(0);
  mpu.setXAccelOffset(0);
  mpu.setYAccelOffset(0);
  mpu.setZAccelOffset(0);

  if (devStatus == 0) {
    Serial.println("Calibrating sensors, keep the IMU still...");
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);

    Serial.println("Enabling DMP...");
    mpu.setDMPEnabled(true);

    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);

    packetSize = mpu.dmpGetFIFOPacketSize();
    dmpReady = true;

    Serial.println("DMP ready.");
    Serial.println("Yaw, Pitch, Roll");
  } else {
    Serial.print("DMP initialization failed, code: ");
    Serial.println(devStatus);
    while (true);
  }
}

void loop() {
  if (!dmpReady) return;

  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

    float yaw   = ypr[0] * 180.0 / M_PI;
    float pitch = ypr[1] * 180.0 / M_PI;
    float roll  = ypr[2] * 180.0 / M_PI;

    Serial.print(yaw);
    Serial.print(", ");
    Serial.print(pitch);
    Serial.print(", ");
    Serial.println(roll);

    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
}
