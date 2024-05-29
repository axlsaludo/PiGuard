# PiGuard
The Pi Guard system enhances security for homes and offices by integrating advanced technologies such as facial recognition, RFID, and the versatile Raspberry Pi. This system seamlessly combines hardware and software components to manage security protocols effectively.

## Modules
1. face_recognizer - main file recognize the persons face and has ui for the rfid reader and manual override
2. face_taker - takes x number of photos of your faces
3. face_train - script that trains the data and stores it in a yml file.
4. rename - python script to automate renaming of files that is same with he naming layout of the face taker.
5. rfid_reader - debug code to read rfid tag from an adrduino sketch.
