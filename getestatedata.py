from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
import datetime
import os
import shutil
from inspect import getsourcefile
from os.path import abspath
from datetime import date
from PIL import Image

gmailUser = ""
gmailPass = ""

class listingInfoParse(object):
    def __init__(self):
        self.title = ""
#--------------------------------------- Importing Stuff ----------------------

file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)
listingsFolderDirectory = os.path.abspath(os.path.join(file_dir, "listings"))
listedFolderDirectory = os.path.join(listingsFolderDirectory,"listed")
chromedriver = file_dir + "/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

#--------------------------------------- Listing Data ----------------------
getting = listingInfoParse()

option = webdriver.ChromeOptions()
#Removes navigator.webdriver flag
# For older ChromeDriver under version 79.0.3945.16
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)

#For ChromeDriver version 79.0.3945.16 or over
option.add_argument('--disable-blink-features=AutomationControlled')

# listing.images = getOrderedListingImages(listingFolder)
getting.driver = webdriver.Chrome(chromedriver, options=option)
getting.driver.get("https://realtor.com")

time.sleep(3)
getting.driver.find_element(By.ID, "searchbox-input").send_keys("2485 kimberly drive, deltona fl 32738")
time.sleep(2)
getting.driver.find_element(By.ID, "searchbox-input").send_keys(Keys.RETURN)

time.sleep(3)
image_tags = getting.driver.find_elements(By.CSS_SELECTOR, "div.slick-track div.slick-slide:not(.slick-cloned)")
count_image = len(image_tags)

img_src = []
if (count_image > 0):
    print ("Extracting Images....")
    for i in range(len(image_tags) - 1):
        img_src.append(getting.driver.find_element(By.CSS_SELECTOR, "div.slick-slide.slick-active img").get_attribute('src'))
        time.sleep(1)
        next_button = getting.driver.find_elements(By.CLASS_NAME, "slick-next")
        for e in next_button:
            e.click()
    img_src.append(getting.driver.find_element(By.CSS_SELECTOR, "div.slick-slide.slick-active img").get_attribute('src'))


time.sleep(3)
price = getting.driver.find_element(By.CLASS_NAME, "rui__sc-62xokl-0").get_attribute('innerHTML')
print("price: "+price)
beds = getting.driver.find_element(By.CSS_SELECTOR, "li.rui__sc-1thjdnb-0 span").get_attribute('innerHTML')
print("beds: "+beds)
bath = getting.driver.find_element(By.CSS_SELECTOR, "li.rui__jalfv4-0 span").get_attribute('innerHTML')
print("bath: "+bath)
sqt = getting.driver.find_element(By.CSS_SELECTOR, "li.rui__sc-147u46e-0 span span").get_attribute('innerHTML')
print("sqft: "+sqt)

getting.driver.close()
# make directory
path = 'images'

# Check whether the specified path exists or not
isExist = os.path.exists(path)

if not isExist:
  
    # Create a new directory because it does not exist 
    os.makedirs(path)

# -- empty directory
folder = 'images'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

if (count_image > 0):
    print ("Saving Images....")
    img_src = list(dict.fromkeys(img_src))
    i = 0
    for item in img_src:
        i = i + 1
        with open('images/'+str(i)+'.jpg', 'wb') as handle:
            response = requests.get(item, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

print ("Done")