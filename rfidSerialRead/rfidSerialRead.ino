#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
Servo myServo; // Create a Servo object

void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();          // Initiate SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  myServo.attach(6);    // Attach the servo to pin 6
  myServo.write(0);     // Initialize the servo position to 0 degrees
  Serial.println("Setup complete. Waiting for RFID card...");
}

void loop() 
{
  // Check for messages to control the servo motor
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "open") {
      myServo.write(180); // Turn servo to 180 degrees
    } else if (command == "close") {
      myServo.write(0); // Turn servo back to 0 degrees
    }
  }

  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
 == 
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  
  // Send UID in a simple format for Python script to read
  Serial.print("UID:");
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println(":END");

  mfrc522.PICC_HaltA(); // Halt PICC

  delay(1000); // Add a delay to prevent flooding the serial output
}
