// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"
#include "SPI.h"
#include "MPU6050_6Axis_MotionApps20.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif
MPU6050 mpu1;
MPU6050 mpu2(0x69); // <-- use for AD0 high

#define OUTPUT_READABLE_YAWPITCHROLL

#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;

// MPU control/status vars
bool dmpReady1 = false;  // set true if DMP init was successful
uint8_t mpuIntStatus1;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize1;    // expected DMP packet size (default is 42 bytes)
uint16_t packetSize2;
uint16_t fifoCount1;     // count of all bytes currently in FIFO
uint8_t fifoBuffer1[64]; // FIFO storage buffer


bool dmpReady2 = false;  // set true if DMP init was successful
uint8_t mpuIntStatus2;   // holds actual interrupt status byte from MPU
uint16_t fifoCount2;     // count of all bytes currently in FIFO
uint8_t fifoBuffer2[64]; // FIFO storage buffer
int zero_detect1,zero_detect2;
// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector
float ypr2[3];
// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };
bool TurnOnZI1 = false;


// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}


void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz). Comment this line if having compilation difficulties with TWBR.
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    Serial.begin(38400);

    mpu1.initialize();
    mpu2.initialize();

    // verify connection
   /*
    mpu1.setAccelerometerPowerOnDelay(3);
    mpu1.setIntZeroMotionEnabled(TurnOnZI1);
    mpu1.setMotionDetectionThreshold(2);
        mpu1.setDHPFMode(1);

    mpu1.setZeroMotionDetectionThreshold(2);
    mpu1.setMotionDetectionDuration(40);
    mpu1.setZeroMotionDetectionDuration(1);
        mpu2.setDHPFMode(1);

    mpu2.setAccelerometerPowerOnDelay(3);
    mpu2.setIntZeroMotionEnabled(TurnOnZI1);
    mpu2.setMotionDetectionThreshold(2);
    mpu2.setZeroMotionDetectionThreshold(2);
    mpu2.setMotionDetectionDuration(40);
    mpu2.setZeroMotionDetectionDuration(1);
    */// wait for ready
    while (Serial.available() && Serial.read()); // empty buffer
    //while (!Serial.available());                 // wait for data
    while (Serial.available() && Serial.read()); // empty buffer again

    // load and configure the DMP
    devStatus = mpu1.dmpInitialize();
    devStatus = mpu2.dmpInitialize();

    // supply your own gyro offsets here, scaled for min sensitivity
/*    mpu1.setXGyroOffset(220);
    mpu1.setYGyroOffset(76);
    mpu1.setZGyroOffset(-85);
    mpu1.setZAccelOffset(1788); // 1688 factory default for my test chip
   mpu2.setXGyroOffset(220);
    mpu2.setYGyroOffset(76);
    mpu2.setZGyroOffset(-85);
    mpu2.setZAccelOffset(1788);
  */  // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // turn on the DMP, now that it's ready
        mpu1.setDMPEnabled(true);

        // enable Arduino interrupt detection
        attachInterrupt(0, dmpDataReady, RISING);
        mpuIntStatus1 = mpu1.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        dmpReady1 = true;

        // get expected DMP packet size for later comparison
        packetSize1 = mpu1.dmpGetFIFOPacketSize();
          mpu2.setDMPEnabled(true);

        // enable Arduino interrupt detection
        attachInterrupt(0, dmpDataReady, RISING);
        mpuIntStatus2 = mpu2.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        dmpReady2 = true;

        // get expected DMP packet size for later comparison
        packetSize2 = mpu2.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)

    }

    // configure LED for output
    pinMode(LED_PIN, OUTPUT);
}



// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {
    // if programming failed, don't try to do anything
  //  zero_detect1 = mpu1.getIntMotionStatus();
   //zero_detect2 = mpu2.getIntMotionStatus();
    if (!dmpReady1) return;

    mpuInterrupt = false;
    mpuIntStatus1 = mpu1.getIntStatus();
   
    // get current FIFO count
    fifoCount1 = mpu1.getFIFOCount();
fifoCount2 = mpu2.getFIFOCount();

    // check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus1 & 0x10) || fifoCount1 == 1024) {
        // reset so we can continue cleanly
        mpu1.resetFIFO();

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus1 & 0x02) {
        // wait for correct available data length, should be a VERY short wait
        while (fifoCount1 < packetSize1) fifoCount1 = mpu1.getFIFOCount();

        // read a packet from FIFO
        mpu1.getFIFOBytes(fifoBuffer1, packetSize1);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount1 -= packetSize1;


        #ifdef OUTPUT_READABLE_YAWPITCHROLL
            // display Euler angles in degrees
            mpu1.dmpGetQuaternion(&q, fifoBuffer1);
            mpu1.dmpGetGravity(&gravity, &q);
            mpu1.dmpGetYawPitchRoll(ypr, &q, &gravity);
            
           
            //Serial.print("\t");
            //Serial.println(zero_detect1);
        #endif

   
 
        // blink LED to indicate activity
        blinkState = !blinkState;
        digitalWrite(LED_PIN, blinkState);
        
          
        
        
        
    }
    if (!dmpReady2) return;

    mpuInterrupt = false;
    mpuIntStatus2 = mpu2.getIntStatus();
   
    // get current FIFO count
    fifoCount2 = mpu2.getFIFOCount();

    // check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus2 & 0x10) || fifoCount2 == 1024) {
        // reset so we can continue cleanly
        mpu2.resetFIFO();

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus2 & 0x02) {
        // wait for correct available data length, should be a VERY short wait
        while (fifoCount2 < packetSize2) fifoCount2 = mpu2.getFIFOCount();

        // read a packet from FIFO
        mpu2.getFIFOBytes(fifoBuffer2, packetSize2);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount2 -= packetSize2;


        #ifdef OUTPUT_READABLE_YAWPITCHROLL
            // display Euler angles in degrees
            mpu2.dmpGetQuaternion(&q, fifoBuffer2);
            mpu2.dmpGetGravity(&gravity, &q);
            mpu2.dmpGetYawPitchRoll(ypr2, &q, &gravity);
             //Serial.print("");
            Serial.print(ypr[0] * 180/M_PI);
            Serial.print("\t");
            Serial.print(ypr[1] * 180/M_PI);
            Serial.print("\t");
            Serial.print(ypr[2] * 180/M_PI);
            Serial.print("\t");
            Serial.print(ypr2[0] * 180/M_PI);
            Serial.print("\t");
            Serial.print(ypr2[1] * 180/M_PI);
            Serial.print("\t");
            Serial.println(ypr2[2] * 180/M_PI);
           // Serial.print("\t");
           // Serial.println(zero_detect2);
        #endif

   
 
        // blink LED to indicate activity
        blinkState = !blinkState;
        digitalWrite(LED_PIN, blinkState);
        
          
   
        
        
    }
    
     
}
