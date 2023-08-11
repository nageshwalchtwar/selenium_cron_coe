import cv2
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import lab_selenium
import logging
import os

logging.basicConfig(filename='lab_latency.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
arr = lab_selenium.timestamps
print(arr)
arr = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in arr]

# moving down click ka timestamp


moving_down = datetime.strptime(lab_selenium.d_movement, '%Y-%m-%d %H:%M:%S')
print("the moving down : ",moving_down)



start_index = 0
end_index = 8

def check_latency(screenshot_paths):
    still_count = 0
    moving_count = 0
    flag = 0
    timestamp1 = None  # Initialize timestamp1 to None

    # Iterate over consecutive pairs of screenshots
    for i in range(start_index, end_index, 2):
        # Load the current and next screenshots
        current_image = 'moving_down_lab/screenshot_{}.png'.format(i)
        next_image = 'moving_down_lab/screenshot_{}.png'.format(i + 1)
        print(current_image)
        print(next_image)

        current_image = cv2.imread(current_image)
        next_image = cv2.imread(next_image)

        # Error handling for image loading
        if current_image is None:
            print(f"Error: Failed to load image {current_image}")
            continue

        if next_image is None:
            print(f"Error: Failed to load image {next_image}")
            continue

        # Compare the current and next screenshots
        gray1 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(next_image, cv2.COLOR_BGR2GRAY)

        similarity_score = ssim(gray1, gray2)
        print(similarity_score)

        # Increment the appropriate counter
        similarity_threshold = 0.99
        if similarity_score >= similarity_threshold:
            print("moving")
            if flag != 1:
                if i < end_index:
                    timestamp1 = arr[i + 1]
                    current_image = 'moving_down_lab/screenshot_{}.png'.format(i)
                    next_image = 'moving_down_lab/screenshot_{}.png'.format(i + 1)
                if not (os.path.exists(current_image) and os.path.exists(next_image)):
                    print(f"Error: Some screenshot files are missing. Skipping iteration {i}.")
                    continue
                print(current_image)
                print(next_image)

                current_image = cv2.imread(current_image)
                next_image = cv2.imread(next_image)

                gray1 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(next_image, cv2.COLOR_BGR2GRAY)

                similarity_score = ssim(gray1, gray2)

                if similarity_score <= similarity_threshold:
                    still_count += 1
                    print("still")
                    # timestamp1= arr[i]
                else:
                    moving_count += 1
                    print("moving")
                    timestamp1 = arr[i+1]
            flag = 1



    latency = (timestamp1 - moving_down).total_seconds()
    logging.info("Latency: %f seconds", latency)


screenshot_paths = []

# Specify the base path and file name format
base_path = "moving_ahead/screenshot_{}.png"

# Specify the range of screenshot numbers


# Generate the screenshot paths
for i in range(start_index, end_index + 1):
    screenshot_path = base_path.format(i)
    screenshot_paths.append(screenshot_path)

# Print the generated screenshot paths
print(screenshot_paths)
check_latency(screenshot_paths)
