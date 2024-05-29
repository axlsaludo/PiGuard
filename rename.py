import os
from datetime import datetime

def rename_images(directory: str, user_id: int):
    """
    Rename all images in a directory with a new naming convention that includes a user ID, a timestamp, and a sequential number.

    Parameters:
        directory (str): The directory containing the images to be renamed.
        user_id (int): The user ID to include in the filename.
    """
    count = 0

    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check if the file is an image
            file_path = os.path.join(directory, filename)
            new_filename = f'Users-{user_id}-{count}.jpg'
            new_file_path = os.path.join(directory, new_filename)

            os.rename(file_path, new_file_path)
            count += 1
            print(f'Renamed {filename} to {new_filename}')

if __name__ == '__main__':
    images_directory = 'images'  # Set the directory containing the images
    user_id = 0  # Set the user ID for the new filenames
    rename_images(images_directory, user_id)
    print('Image renaming complete.')
