/*
  This example creates a BLE central that scans for a peripheral with a Test Service
  If that contains floatValue characteristics the value can be seen in the Serial Monitor or Plotter.

  The circuit:
  - Arduino Nano 33 BLE or Arduino Nano 33 IoT board.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
//----------------------------------------------------------------------------------------------------------------------
// BLE UUIDs
//----------------------------------------------------------------------------------------------------------------------

#define BLE_UUID_TEST_SERVICE   "9A48ECBA-2E92-082F-C079-9E75AAE428B1"
#define BLE_UUID_FLOAT_VALUE1   "C8F88594-2217-0CA6-8F06-A4270B675D69"
#define BLE_UUID_FLOAT_VALUE2   "C8F88594-2217-0CA6-8F06-A4270B675D70"
#define BLE_UUID_FLOAT_VALUE3   "C8F88594-2217-0CA6-8F06-A4270B675D68"
#define BLE_UUID_AMPLITUDE      "E3ADBF53-950E-DC1D-9B44-076BE52760D6"



BLEService testService( BLE_UUID_TEST_SERVICE );
BLEFloatCharacteristic floatValueCharacteristicX( BLE_UUID_FLOAT_VALUE1, BLERead | BLENotify );
BLEFloatCharacteristic floatValueCharacteristicY( BLE_UUID_FLOAT_VALUE2, BLERead | BLENotify );
BLEFloatCharacteristic floatValueCharacteristicZ( BLE_UUID_FLOAT_VALUE3, BLERead | BLENotify );
BLEFloatCharacteristic amplitudeCharacteristic( BLE_UUID_AMPLITUDE, BLERead | BLEWrite );

float floatValue = 0.0;
float amplitude = 0.1;
float x_init=0.0, y_init=0.0, z_init=0.0;
float current_x=0.0, current_y=0.0, current_z=0.0;
float diff=0.0;
long previousMillis = 0;  // last time the tap checked, in ms
float tap=0.0;

void setup()
{
//    Serial.begin(9600);
//    while (!Serial);
//    Serial.println("Started");

    if (!IMU.begin()) {
//        Serial.println("Failed to initialize IMU!");
        while (1);
    }

    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(current_x, current_y, current_z);
    }

    if (!BLE.begin()) {
//        Serial.println("Starting BLE failed!");
        while (1);
    }

    // set advertised local name and service UUID:
    BLE.setLocalName("Left Motion Band");
    BLE.setAdvertisedService(testService);

    // add the characteristic to the service
    testService.addCharacteristic(floatValueCharacteristicX);
    testService.addCharacteristic(floatValueCharacteristicY);
    testService.addCharacteristic( floatValueCharacteristicZ);
    testService.addCharacteristic(amplitudeCharacteristic);

    BLE.addService(testService);
    floatValueCharacteristicX.writeValue(floatValue); // set initial value
    floatValueCharacteristicY.writeValue(floatValue); // set initial value
    floatValueCharacteristicZ.writeValue(floatValue);
    amplitudeCharacteristic.writeValue(amplitude); // set initial value

    // start advertising
    BLE.advertise();

    // Print out full UUID and MAC address.
//    Serial.println("Peripheral advertising info: ");
//    Serial.print("MAC: ");
//    Serial.println(BLE.address());
//    Serial.print("Service UUID: ");
//    Serial.println(testService.uuid());

//    Serial.println(" Arduino Nano BLE LED Peripheral Service Started");
}




void loop()
{
    BLEDevice central = BLE.central();

    if (central)
    {
        while (central.connected()){
            x_init=current_x;
            y_init=current_y;
            z_init=current_z;

            if (IMU.accelerationAvailable()){
                IMU.readAcceleration(current_x, current_y, current_z);
                diff=current_z-z_init;
    
                if(diff < -0.5){
                    long currentMillis = millis();
                    if (currentMillis - previousMillis >= 500) {
                        previousMillis = currentMillis;
//                        Serial.println("tap is detected");
                        tap=1.0;
                    }
                }
  
                if (tap==1.0){
                  floatValueCharacteristicZ.writeValue(diff);
//                  Serial.print(current_z);
//                  Serial.println();
                  tap=0.0;
                }
   
            }
        }
   }
}
