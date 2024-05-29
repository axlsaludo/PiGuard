import cv2
import numpy as np
from PIL import Image
import os
import logging

def getImagesAndLabels(path):
    """
    Load face images and corresponding labels from the given directory path.

    Parameters:
        path (str): Directory path containing face images.

    Returns:
        list: List of face samples.
        list: List of corresponding labels.
    """
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg") or f.endswith(".png")]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            # Convert image to grayscale
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            # Extract the user ID from the image file name
            id = int(os.path.split(imagePath)[-1].split("-")[1])

            # Detect faces in the grayscale image
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                # Extract face region and append to the samples
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        except Exception as e:
            logging.error(f"Failed to process image {imagePath}: {e}")

    return faceSamples, ids

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Directory path where the face images are stored.
    path = './images/'
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Haar cascade file for face detection
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    logging.info("[INFO] Training...")

    faces, ids = getImagesAndLabels(path)

    # Train the recognizer with the face samples and corresponding labels
    if faces and ids:
        recognizer.train(faces, np.array(ids))

        # Save the trained model into the current directory
        recognizer.write('trainer.yml')

        logging.info(f"[INFO] {len(np.unique(ids))} faces trained from {len(faces)} images. Exiting Program")
    else:
        logging.info("[INFO] No faces found for training.")
