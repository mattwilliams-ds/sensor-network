// A script for taking temperature & humidity sensor readings
// and writing the data to the serial port.

#include "DHT.h"
#define dht11_pin 2

DHT dht11(dht11_pin, DHT11);


void setup() {
  Serial.begin(9600); // set baud rate
  dht11.begin();      // initialize the sensor
}

void loop() {
  // Read ambient humidity & temperature (F)
  float humidity = dht11.readHumidity();
  float temperature = dht11.readTemperature(true);

  // Correct readings
  float scaled_humidity = humidity * 51/21.6;
  float scaled_temperature = temperature * 2.206;

  // Output data to the serial port
  Serial.print(scaled_humidity);
  Serial.print(":");
  Serial.print(scaled_temperature);
  Serial.print("\n");

  delay(2000);        // pause 2s before re-running loop
}
