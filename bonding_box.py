import cv2
from skimage.metrics import structural_similarity as ssim
import os 
import re
from dotenv import load_dotenv
import logging
from email.message import EmailMessage
import ssl
import smtplib
import time
import subprocess

import ss_4_lab
# import every_image_cmp


load_dotenv()
# comapre each screenshot script ( impprt every_screenshot ) starts /

import os
import cv2
from skimage.metrics import structural_similarity as ssim

def compare_images(image1, image2):
    # Load the images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    
    # Convert images to grayscale for SSIM computation
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM
    similarity = ssim(gray_img1, gray_img2)
    
    return similarity

def compare_images_in_folder(folder_path):
    # Get a list of all image files in the folder
    image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    min_similarity = 1.0  # Initialize with the maximum value
    dissimilar_image_pair = None
    
    # Compare each image with every other image in the folder
    for i in range(len(image_files)):
        for j in range(i + 1, len(image_files)):
            image1_path = os.path.join(folder_path, image_files[i])
            image2_path = os.path.join(folder_path, image_files[j])
            
            similarity = compare_images(image1_path, image2_path)
            
            # Update the minimum similarity and image pair if the current similarity is lower
            if similarity < min_similarity:
                min_similarity = similarity
                dissimilar_image_pair = (image_files[i], image_files[j])
    
    if dissimilar_image_pair is not None:
        print(f"The most dissimilar images are {dissimilar_image_pair[0]} and {dissimilar_image_pair[1]}")
        print(f"Dissimilarity score: {min_similarity}")
        
        # Load the most dissimilar images
        img1 = cv2.imread(os.path.join(folder_path, dissimilar_image_pair[0]))
        img2 = cv2.imread(os.path.join(folder_path, dissimilar_image_pair[1]))
        
        # Convert images to grayscale for contour detection
        gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Find contours in the images
        contours1, _ = cv2.findContours(gray_img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(gray_img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on the images
        cv2.drawContours(img1, contours1, -1, (0, 0, 255), 2)
        cv2.drawContours(img2, contours2, -1, (0, 0, 255), 2)
        
        # # Display the images with contours
        # cv2.imshow("Image 1", img1)
        # cv2.imshow("Image 2", img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return min_similarity
    else:
        global no_dis
        no_dis=1
        print("No dissimilar image pairs found in the folder")


folder_path = "moving_ahead/"

# Call the function to compare images in the folder
comparison = compare_images_in_folder(folder_path)
print("the dissimilarity is :",comparison)
# comapre screenshot ends /
            
if comparison >= 0.96:
    global movement_code
    movement_code = 1
    print("Experiment is working fine, because there are dissimilar images .")
else:
    movement_code= 0
    print("Experiment is not working .")


chk_latency= ss_4_lab.check_latency
#logging all the data 
logging.basicConfig(filename='lab_position.log', filemode='a',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
#sending imp update mails 
def send_email(person, body, email_subject):
    email_sender = 'rtllab55@gmail.com'
    email_password = 'evyvskiyltlczpaj'
    email_receiver = person
    msg = EmailMessage()
    msg.set_content(body)

    # Set the email parameters
    msg['Subject'] = 'RTL - Maintainance update ( COE )'
    msg['From'] = email_sender
    msg['To'] = ', '.join(recipients)  # Join the list of recipients

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())

ss_paths = ss_4_lab.ss_paths



    

if movement_code == 0:
    logging.warning('still\n')
    global status 
    status = "Not Working"
    recipients = ["nageshwalchtwar257@gmail.com", "vedant.nipane@students.iiit.ac.in","rishabh.agrawal@students.iiit.ac.in","abhinav.marri@research.iiit.ac.in"]
    send_email(recipients, '''Hi, I'm COE,
                Experiment is having some issue,the experiment is stucked or Video stream is not available during the process.
                kindly check the experiment.
                - Maintenance Team ( RTL - SPCRC )


                
       This is a script generated alert, do not reply to it.''', 'mail sent')

elif  movement_code == 1:
    logging.info('Working Fine.\n')
    status = "working"
    recipients = ["theccbussiness@gmail.com"]
    send_email(recipients, '''Hi, I'm COE, experiment working fine.
                - Maintenance Team ( RTL - SPCRC )

                
        This is a script generated alert, do not reply to it.''', 'mail sent')

import json

data = {
    "value": status
}

with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

# Add, commit, and push the changes
subprocess.run(["git", "add", "data.json"])
subprocess.run(["git", "commit", "-m", "Update data.json"])
subprocess.run(["git", "push", "origin", "main"]) 


