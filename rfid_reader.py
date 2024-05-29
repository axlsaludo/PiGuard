import serial

AUTHORIZED_UID = "61 44 CD 06"  # The specific UID that is authorized to unlock the door

def read_rfid_tag(port='COM3', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            uid = ser.readline().decode().strip()
            if uid == AUTHORIZED_UID:
                return True  # Authorized
            return False  # Not authorized
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return False  # Communication error or other issue
    