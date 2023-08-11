import cv2
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import lab_selenium
import logging
import os
import re
logging.basicConfig(filename='lab_latency.log', filemode='a',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
arr = lab_selenium.timestamps
print(arr)
arr = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in arr]


#importing data from the log files 
log_file_path= "lab_latency.log"

if os.path.exists(log_file_path):
    pass
else:
    print('Log file not found by the RTL Server.')



pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - Latency: (\d+\.\d+) seconds"
with open(log_file_path,'r') as file:
    log_data=file.read()
matches= re.findall(pattern,log_data)
for match in matches:
    timestamp, latency=match
    
# moving down click ka timestamp
moving_down  = datetime.strptime(lab_selenium.d_movement, '%Y-%m-%d %H:%M:%S')
print(moving_down)
status = ""
start_index = 0
end_index = 9
mail_service=lab_selenium.handle_prompt
def check_latency(screenshot_paths): 
    still_count = 0
    moving_count = 0
    flag=0
    # Iterate over consecutive pairs of screenshots
    for i in range(0,end_index+1,2):
        # Load the current and next screenshots
        # The dynamic number
        current_image = 'moving_ahead/screenshot_{}.png'.format(i)
        next_image  = 'moving_ahead/screenshot_{}.png'.format(i+2)
        print(current_image)
        print(next_image)

        current_image = cv2.imread(current_image)
        next_image = cv2.imread(next_image)

        # Compare the current and next screenshots
        # similarity_score = compare_images(current_image, next_image)
        gray1 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(next_image, cv2.COLOR_BGR2GRAY)

        similarity_score = ssim(gray1, gray2)
        print(similarity_score)


        # Increment the appropriate counter
        similarity_threshold = 0.98
        if similarity_score >= similarity_threshold:
            print("moving")
            
            if flag!=1:
                # print("still --> moving")
                # Timestamp 1ṇṇ
                #timestamp1 = datetime.now()
                timestamp1 = arr[i+1]
                current_image = 'moving_ahead/screenshot_{}.png'.format(i)
                next_image  = 'moving_ahead/screenshot_{}.png'.format(i+1)
                print(current_image)
                print(next_image)

                current_image = cv2.imread(current_image)
                next_image = cv2.imread(next_image)

                # Compare the current and next screenshots.
                # similarity_score = compare_images(current_image, next_image)
                gray1 = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(next_image, cv2.COLOR_BGR2GRAY)

                similarity_score = ssim(gray1, gray2)

                if similarity_score <= similarity_threshold:
                    still_count += 1
                    print("still")
                    #time_diff-=2
                    # logging.info(timestamp1)

                else:
                    moving_count+=1
                    print("moving")
                    status="moving"
                    timestamp1 = arr[i]
                    # logging.info(timestamp1)
                    
            flag=1
            

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
