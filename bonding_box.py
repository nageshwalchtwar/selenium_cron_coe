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

import ss_4_lab
import every_image_cmp


load_dotenv()

chk_latency= ss_4_lab.check_latency
comp= every_image_cmp.compare_images_in_folder
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
# def process_image(image1, image2):
#     # Convert the images to grayscale
#     gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
#     gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

#     # Compute the absolute difference between the two grayscale images
#     diff = cv2.absdiff(gray1, gray2)

#     # Apply a threshold to create a binary image
#     threshold = 35  # Adjust the threshold as needed
#     _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
#     # cv2.imshow("diff : ", diff)    # Find contours in the thresholded image
#     contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Define the minimum and maximum areas for bounding boxes
#     min_area = 100  # Minimum area threshold for bounding boxes
#     max_area = 5000  # Maximum area threshold for bounding boxes

#     # Store the coordinates of bounding boxes in a list of tuples
#     bounding_boxes = []

#     # Draw bounding boxes around the contours within the specified area range
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if min_area <= area <= max_area:
#             x, y, w, h = cv2.boundingRect(contour)
#             bounding_boxes.append((x, y))
#             cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     # Display the image with filtered bounding boxes
#     cv2.imshow("Image with Filtered Bounding Boxes 1", image1)
#     cv2.imshow("Image with Filtered Bounding Boxes 2", image2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     # print(image1.shape)
#     # print(image2.shape)
#     # Return the list of bounding boxes
#     return bounding_boxes


def compare_images(image1, image2):
    
    # #convet to image
    # im1= cv2.imread(image1)
    # im2= cv2.imread(image2)
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute the SSIM score
    similarity_score = ssim(gray1, gray2)
    # print("similarity score " ,similarity_score)

    # Set the similarity threshold
    similarity_threshold = 0.99
    

    if similarity_score >= similarity_threshold:
        return 0 
    else:
        return 1

#checking the latency and extr̥acting the 4 ss to comapare

#comapring the ss from the folder
# def compare_ss(file_path_ss):
#     print('comparing the images ...')
#     img_path1 = file_path_ss + 'screenshot_0.png'
#     img_path2 = file_path_ss + 'screenshot_9.png'

#     img1 = cv2.imread(img_path1)
#     img2 = cv2.imread(img_path2)
    
#     if compare_images(img1,img2) == 0:
#         print('Ball is still')
#         return "still" 
#     else:
#         if file_path_ss == "moving_ahead/":
#             img_path1,img_path2,img_path3,img_path4 = ss_paths[0:4]
#         else:
#             img_path1,img_path2,img_path3,img_path4 = ss_paths[4:]
    
#     bounding_boxes1 = process_image(img_path1,img_path2)
#     bounding_boxes2 = process_image(img_path3,img_path4)

#     print('motion .. ')

#     sorted_arr1 = sorted(bounding_boxes1, key =lambda x: x[0])
#     sorted_arr2 = sorted(bounding_boxes2, key =lambda x: x[0])
#     com= compare_images(sorted_arr1,sorted_arr2)
#     print(com)
#     # if com==0:
#     #     print('no motion')
#     # else:
#     #     print('motion')
#     associations = []
#     for point2 in sorted_arr2:
#         min_distance = 25
#         associated_point = None
        
#         for point1 in sorted_arr1:
#             distance = abs(point2[0] - point1[0])
#             if distance < min_distance:
#                 min_distance = distance
#                 associated_point = point1
                
#         if associated_point:
#             associations.append((associated_point, point2))
    
#     distances = []
#     for association in associations:
#         dist = association[1][1] - association[0][1]
#         distances.append(dist)
#         print('distances' ,distances)
#         if distances[0]<=0:
#             return 'still'
#         else:
#             return 'moving'
        
    
#         # if distances[0] < 0:
#         #     return "up"
#         # else:
#         #     return "down"



    
file_path_ss = "moving_ahead/"
image_path1 = "moving_ahead/screenshot_1.png"
image_path2 = "moving_ahead/screenshot_9.png"

image1 = cv2.imread(image_path1)
image2 = cv2.imread(image_path2)

# bounding_boxes = process_image(image1, image2)
movement_code = compare_images(image1, image2)


# print("Bounding boxes:", bounding_boxes)
# print("Movement code:", movement_code)

print(comp)


# l= f"moving_ahead/"
# for i in range(len(l)):
#     movement_code= compare_ss(ss_paths)
#     if movement_code == 'still':
#         logging.warning('Motion\n')
#     elif movement_code == 'moving':
#         logging.info('moving\n')
#     else:
#         logging.debug("Error, check system ASAP!")
print(chk_latency)  
if movement_code == "still" or movement_code == 0:
    logging.warning('still\n')
    recipients = ["nageshwalchtwar257@gmail.com", "vedant.nipane@students.iiit.ac.in","rishabh.agrawal@students.iiit.ac.in","abhinav.marri@research.iiit.ac.in"]
    send_email(recipients, '''Hi, I'm COE,
                Experiment is having some issue,
                The experiment is stucked or Video stream not available during the process.
                kindly check the experiment.
                - Maintenance Team ( RTL - SPCRC )


                
       This is a script generated alert, do not reply to it.''', 'mail sent')

elif movement_code == 'moving' or movement_code == 1:
    logging.info('Working Fine.\n')
    recipients = ["theccbussiness@gmail.com"]
    send_email(recipients, '''Hi, I'm COE, experiment working fine.
                - Maintenance Team ( RTL - SPCRC )

                
        This is a script generated alert, do not reply to it.''', 'mail sent')



# print(direction_check)
