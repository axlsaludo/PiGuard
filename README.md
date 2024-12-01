
![top](https://github.com/user-attachments/assets/590094fa-ea04-48e8-b4dc-d062c1ab11d0)

---

# PiGuard
The Pi Guard system enhances security for homes and offices by integrating advanced technologies such as facial recognition, RFID, and the versatile Raspberry Pi. This system seamlessly combines hardware and software components to manage security protocols effectively.

## Components
- Arduino Uno or Nano
- Raspberry PI or Laptop
- Servo Motor
- RC522 RFID Reader
- RFID Card
- Connecting Wires
- Webcam


## Modules
1. face_recognizer - main file recognize the persons face and has ui for the rfid reader and manual override
2. face_taker - takes x number of photos of your faces
3. face_train - script that trains the data and stores it in a yml file.
4. rename - python script to automate renaming of files that is same with he naming layout of the face taker.
5. rfid_reader - debug code to read rfid tag from an adrduino sketch.
6. rfidSerialRead - arduino code for the servomotor and the rc522 to read and send data using serial communcation

---

### Circuit Schematic

![image](https://github.com/ewanmoak/PiGuard/assets/79072016/d94dd4cb-f7d7-4fcc-b265-2f3def6b3020)


### Circuit Block Diagram

![blcok diagram](https://github.com/ewanmoak/PiGuard/assets/79072016/41abe3f5-e8a1-4868-b3ab-c6655104699a)
