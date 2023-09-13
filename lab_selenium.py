import os
os.environ['DISPLAY'] = ':99'
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np
from PIL import Image
from email.message import EmailMessage
import ssl
import smtplib
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from email.message import EmailMessage
import subprocess
import datetime
import imagehash
from dotenv import load_dotenv
from skimage.metrics import structural_similarity as ssim
import json
# timestamps.py
move = 0
timestamps = []
d_movement = ""

def update_timestamps(new_timestamp):
    global timestamps
    timestamps.append(new_timestamp)


global status 
global msgs 


load_dotenv()
total = 0
 # Set webdriver options

# chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

# chrome_options = Options()
# options = [
#     "--headless",
#     "--disable-gpu",
#     "--window-size=1920,1200",
#     "--ignore-certificate-errors",
#     "--disable-extensions",
#     "--no-sandbox",
#     "--disable-dev-shm-usage"
# ]
# for option in options:
#     chrome_options.add_argument(option)
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver = webdriver.Firefox()

# Load the updated YAML file
with open('lab_data.yaml', 'r') as file:
    actions = yaml.safe_load(file)


def process_video_frames(driver: webdriver.Chrome, video_xpath: str):
    global move
    screenshot_paths = []
    total_screenshots, interval = 10, 0.5
    video_element = driver.find_element(By.XPATH, video_xpath)

    for i in range(total_screenshots):
        video_screenshot = video_element.screenshot_as_png
        update_timestamps(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if move == 0:
            screenshot_file = f"moving_ahead/screenshot_{i}.png"
        else:
            screenshot_file = f"moving_ahead/screenshot_{i}.png"

        with open(screenshot_file, "wb") as file:
            file.write(video_screenshot)

        screenshot_paths.append(screenshot_file)
        time.sleep(interval)
    move += 1
    print(timestamps)
    print("detecting motion")
    

def send_email(person, body, email_subject,recipients=None):
    email_sender = 'rtllab55@gmail.com'
    email_password = 'evyvskiyltlczpaj'
    email_receiver = person
    msg = EmailMessage()
    msg.set_content(body)
    # Set the email parameters
    msg['Subject'] = 'RTL issue'
    msg['From'] = email_sender
    msg['To'] = ', '.join(recipients)  # Join the list of recipients
    
    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', context=context) as smtp:
        recipients = ["nageshwalchtwar257@gmail.com", "vedant.nipane@students.iiit.ac.in","rishabh.agrawal@students.iiit.ac.in","abhinav.marri@research.iiit.ac.in"]
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, recipients, msg.as_string())

def handle_prompt(prompt_text, email_recipient=None, email_subject=None):
    if prompt_text == "Experiment is currently offline" or prompt_text == "Experiment is currently in use":
        body = "Experiment is currently offline (COE)"
        msgs = "OFFLINE"
        data = {
            "value": msgs
        }

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)

        # Add, commit, and push the changes
        subprocess.run(["git", "add", "data.json"])
        subprocess.run(["git", "commit", "-m", "Update data.json"])
        subprocess.run(["git", "push", "origin", "main"]) 

        if email_recipient and email_subject:
            send_email(email_recipient, body, email_subject)
        try:
            driver.switch_to.alert.accept()
        except UnexpectedAlertPresentException:
            pass
        return True  # Set the flag to True indicating prompt is handled
    elif prompt_text == "Experiment is currently in use":
        msgs ="In Use - Script will execute after some time "
        driver.switch_to.alert.accept()
        data = {
                "value": msgs
        }

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)

        # Add, commit, and push the changes
        subprocess.run(["git", "add", "data.json"])
        subprocess.run(["git", "commit", "-m", "Update data.json"])
        subprocess.run(["git", "push", "origin", "main"]) 

        return True  # Set the flag to True indicating prompt is handled
    return False  # Return False if prompt is not handled

# Define a function to perform actions on web elements
def perform_action(element):
    global total

    if total == 2:
        value = os.getenv('PASSWORD')
    else:
        value = element.get('value')

    locator_strategy = element['locator_strategy']
    locator_value = element['locator_value']
    action = element['action']

    try:
        if locator_strategy == 'id':
            time.sleep(10)
            web_element = driver.find_element(By.ID, locator_value)
        elif locator_strategy == 'xpath':
            # time.sleep(5)
            web_element = driver.find_element(By.XPATH, locator_value)
        elif locator_strategy == 'coe':
            pass
        # Add more locator strategies if needed
    except NoSuchElementException:
        web_element= driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[1]/div/div[3]/div[3]/button[2]')
        web_element.click()
        print("Testing ended abruptly!!!")

    # Perform actions on the web element
    if action == 'input':
        web_element.send_keys(value)
    elif action == 'click':
        time.sleep(5)
        # if(len(list(web_element)) >= 3):
        #     web_element[2].click()
        # else:
        if locator_value == "//*[contains(text(), 'Start Experiment')]" :
            global d_movement
            d_movement = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            web_element.click()
        elif locator_value == "Conservation of Mechanical Energy":
            script = """
            var parentDiv = document.querySelector(".-mt-12");
            parentDiv.style.opacity = '1';
            parentDiv.scrollIntoView(true);
            """
            driver.execute_script(script)
            time.sleep(3)
            button = driver.find_element(By.ID, "Conservation of Mechanical Energy")
            button.click()
        else:
            web_element.click()

    elif action == 'process_video_frames':
        process_video_frames(driver, locator_value)
    elif action == 'handle_prompt':
        while True:
            time.sleep(10)
            try:
                alert = driver.switch_to.alert
                prompt_text = alert.text
                prompts = element.get('prompts')
                if prompts:
                    for prompt in prompts:
                        if prompt['prompt_text'] == prompt_text:
                            email_recipient = prompt.get('email_recipient')
                            email_subject = prompt.get('email_subject')
                            if handle_prompt(prompt_text, email_recipient, email_subject):
                                exit()
                                break  # Break out of the inner loop if prompt is handled
                    else:
                        break  # Break out of the outer loop if prompt is not handled
                else:
                    break  # Break out of the outer loop if no prompts are specified
            except NoAlertPresentException:
                break  # Break out of the outer loop if no alert is present

# Load the website
driver.get('https://remote-labs.in')
time.sleep(3)

# Perform the actions specified in the YAML file
for action in actions:
    print(action)
    if total <= 1:
        total += 1
        status = "Working"
    else:
        status = "Not working or OFFLINE"
        
        
    perform_action(action)


    data = {
        "value": status
    }

    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    # Add, commit, and push the changes
    subprocess.run(["git", "add", "data.json"])
    subprocess.run(["git", "commit", "-m", "Update data.json"])
    subprocess.run(["git", "push", "origin", "main"]) 
    time.sleep(2)
