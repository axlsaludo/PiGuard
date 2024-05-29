import cv2
import numpy as np
import json
import serial
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# Load valid UIDs from a file or define them here
valid_uids = {"6144CD06": "axl", "87654321": "person2"}  # Mapping UIDs to names

# Load face names from a JSON file
try:
    with open('names.json', 'r') as file:
        names = json.load(file)
    print(f"Loaded names: {names}")
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading names.json: {e}")
    names = {"0": "Unknown"}  # Default name if loading fails

# Setup serial connection
def setup_serial(port="COM3"):
    try:
        return serial.Serial(port=port, baudrate=9600, timeout=1)
    except serial.SerialException:
        print(f"No device connected on {port}")
        return None

serial_connection = setup_serial()

def read_rfid():
    if serial_connection is not None and serial_connection.in_waiting > 0:
        uid = serial_connection.readline().decode().strip()
        uid = uid.replace(" ", "")
        if uid in valid_uids:
            return uid, "Valid", valid_uids[uid]
        else:
            return uid, "Invalid", None
    return None, "Not Checked", None

def update_gui(image, face_status, rfid_status, door_status):
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(image))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)

    face_indicator.config(text=f"Face Status: {face_status}", bg=door_status)
    rfid_indicator.config(text=f"RFID Status: {rfid_status}", bg=door_status)
    door_state_indicator.config(text=f"Door State: {'Unlocked' if door_status == 'green' else 'Locked'}", bg=door_status)

    window.update_idletasks()

def lock_door():
    global door_unlocked
    door_unlocked = False
    door_state_indicator.config(text="Door State: Locked", bg="red")

def on_closing():
    window.destroy()
    cam.release()
    cv2.destroyAllWindows()
    if serial_connection:
        serial_connection.close()

# Main function
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Face and RFID Recognition")

    lmain = tk.Label(window)
    lmain.pack()

    face_indicator = Label(window, text="Face Status: Not Checked", bg="yellow", font=("Arial", 16))
    face_indicator.pack(side="right", fill="both", expand="yes", padx=10, pady=10)

    rfid_indicator = Label(window, text="RFID Status: Not Checked", bg="yellow", font=("Arial", 16))
    rfid_indicator.pack(side="right", fill="both", expand="yes", padx=10, pady=10)

    cam = cv2.VideoCapture(0)
    cam.set(3, 1280)
    cam.set(4, 720)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Second window for door status
    door_window = tk.Toplevel(window)
    door_window.title("Door Control")

    door_state_indicator = Label(door_window, text="Door State: Locked", bg="red", font=("Arial", 16))
    door_state_indicator.pack(pady=20)

    lock_button = Button(door_window, text="Lock Door", command=lock_door, font=("Arial", 16))
    lock_button.pack(pady=20)

    # Ensure both windows close the program
    window.protocol("WM_DELETE_WINDOW", on_closing)
    door_window.protocol("WM_DELETE_WINDOW", on_closing)

    door_unlocked = False

    def process_frame():
        global door_unlocked

        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame")
            window.after(10, process_frame)
            return

        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(0.1 * cam.get(3)), int(0.1 * cam.get(4))),
        )

        uid, rfid_status, associated_name = read_rfid()

        face_status = "No Face Detected"
        door_status = "red" if not door_unlocked else "green"
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            str_id = str(id)
            if str_id in names and confidence < 60:
                face_status = f"{names[str_id]}, {confidence:.2f}% Confidence"
                if names[str_id] == associated_name:
                    door_unlocked = True
                    face_status += " - Door Unlocked"
                    rfid_status += " - Door Unlocked"
                    door_status = "green"

        update_gui(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), face_status, rfid_status, door_status)

        window.after(10, process_frame)

    window.after(10, process_frame)
    window.mainloop()
