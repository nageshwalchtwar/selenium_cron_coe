# this code is only to check the similarity betn the screenshots in the folder using cv.

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
        print("No dissimilar image pairs found in the folder")


folder_path = "moving_ahead/"

# Call the function to compare images in the folder
comparison = compare_images_in_folder(folder_path)

if comparison==1:
    print("experiment is wokring fine .")
elif comparison==0:
    print("experiment is not working .")
