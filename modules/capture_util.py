#import required modules
import os, cv2, random, uuid
from datetime import datetime
from pathlib import Path

DATA_ROOT = 'frames'

#save a frame into a random folder to avoid SD card crash
def random_save(image, total_folder, folder_prefix='folder'):
    # Create n folders if they don't exist
    for i in range(total_folder):
        folder_path = f"{folder_prefix}_{i+1}"
        os.makedirs(os.path.join(DATA_ROOT, folder_path), exist_ok=True)

    # Randomly select a folder to save the image
    random_folder = random.randint(1, total_folder)
    selected_folder = f"{folder_prefix}_{random_folder}"

    #define a name for image based on current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]

    # Save the image to the selected folder
    image_name = f"{current_time}_frame_{str(uuid.uuid4())[:5]}.jpg"
    image_path = os.path.join(DATA_ROOT, selected_folder, image_name)
    cv2.imwrite(image_path, image)

    return selected_folder, image_path