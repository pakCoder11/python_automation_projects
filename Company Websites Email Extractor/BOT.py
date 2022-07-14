import csv
import os
from selenium import webdriver
import re
import time
import pyautogui
import mss
import mss.tools
import json
import requests
from PIL import Image
from bs4 import BeautifulSoup
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Method to read data from JSON file 
def read_data_from_json():
    """
    Read data from JSON file...
    """
    with open('config.json') as f:
        data = json.load(f)

    return data

def take_screenshot(left,top,width,height,output_image):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"left": left, "top": top, "width": width+200, "height": height}

        # Grab the data
        sct_img = sct.grab(monitor)
        path = os.getcwd() + '\\images\\' + output_image
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=path)

def readImage(picture):
    # this function is used to read text from the image and turn into list.

    # from PIL.Image import core as image
    img = Image.open(picture)
    text = tess.image_to_string(img)
    text_string = str(text)
    lister = text_string.splitlines()
    return lister


def LocateImageOnScreen(image_png):

    # this function is used to search the image on screen and returns the co-ordinates
    # time.sleep(4)

    if pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8) != None:
        cordinates = pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8)
        return cordinates
    else:
        return []


def Pressdown_keyboard(number_of_press_down):

    # this function is used to press the 'Down' key from keyboard automatically        
    for i in range(0,number_of_press_down):
        pyautogui.press('down')

def read_urls_():
    """
    This function is used to read 
    """

    with open("links.txt","r") as file: 
        data = file.readlines()

    return data

def start_web_driver(path):

    """
    This function is used to start the google web driver
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=path,options=chrome_options)
    driver.maximize_window()

    return driver 

def get_contact_us_page(website_link,url_list):
    """
    This function is used to get the URL of Contact US page
    return: string
    # get_contact_us_page(website_link,href_list)

    """

    string = ""
    for url in url_list:
        string = url
        if string.find('contact') >=0 or string.find('about-us') >=0:
            break 

    if string.find('contact') >= 0 or string.find('about-us') >= 0:

        if string.find('http') == 0:
            return string 
        else:
            return website_link + string
    else:
        return ""

def parse_email_list_to_string(list_of_email_addresses):
    """
    This function is used to covert the list of emails to string 
    ['saadkhan6031@gmail.com','saadkhang106031@yahoo.com'] to saadkhan6031@gmail.com, saadkhang106031@yahoo.com
    """

    # using list comprehension 
    emailStr = ' ,'.join([str(element) for element in list_of_email_addresses]) 
    return emailStr

def extract_email(website_link,contact_page_url,status_code):
    """
    This function is used to scrap the email address from the website
    This function uses the following approach to extract details of email
    
    status_code = 200 scrap source through HTTP requests library, otherwise use Selenium webdriver to scrap source code of website

    (1) Open contact page of website 
    (2) Extract source code of the website 
    (3) Run the regex on source code to extract email address
    (4) All emails will be stored in the dictionary
    """

    # if function recieves contact page url
    if len(contact_page_url) > 0 and status_code == 200: 
        print("Contact page was found and status_code is 200")

        page = requests.get(contact_page_url)
        soup = BeautifulSoup(page.content,'html.parser')
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup))
        email_string = parse_email_list_to_string(emails)
        data_dictionary['Email'] = email_string
        # print(email_string)

    elif len(contact_page_url) == 0 and status_code == 200: 
        print("Contact page was not found and status_code is 200")
        page = requests.get(website_link)
        soup = BeautifulSoup(page.content,'html.parser')
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup))
        email_string = parse_email_list_to_string(emails)
        data_dictionary['Email'] = email_string
        # print(email_string)

    elif len(contact_page_url) > 0 and status_code != 200:

        print("Contact pase was found but Status code is not 200")
        browser = start_web_driver(chromedriver_path)
        browser.get(contact_page_url)
        source_code = browser.find_element_by_tag_name("body").get_attribute("innerHTML")
        soup = BeautifulSoup(source_code,'html.parser')
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup))
        email_string = parse_email_list_to_string(emails)
        data_dictionary['Email'] = email_string
        # print(email_string)        

    elif len(contact_page_url) == 0 and status_code != 200: 
        print("Contact pase was not found and Status code is also not 200")

        browser = start_web_driver(chromedriver_path)
        browser.get(website_link)
        source_code = browser.find_element_by_tag_name("body").get_attribute("innerHTML")
        soup = BeautifulSoup(source_code,'html.parser')
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", str(soup))
        email_string = parse_email_list_to_string(emails)
        data_dictionary['Email'] = email_string

        # print(email_string)  

def extract_social_media_links(urls_list): 
    """
    This function is used to get the links of social media accounts...
    like Facebook, Twitter, Instagram & LinkedIn
    """
    social_media_links = []

    for url in urls_list:

        string = url 
        if string.find('facebook.com') >=0 or string.find('instagram.com') >=0 or string.find('twitter.com') >=0 or string.find('linkedin.com') >=0 or string.find('tiktok.com') >=0:
            social_media_links.append(string)            

    # when the list of social media links was found, so we will store them all into dictionary
    if len(social_media_links) > 0:

        for sml in social_media_links:

            if sml.find('facebook.com') >= 0: 
                data_dictionary['Facebook Page'] = sml

            elif sml.find('instagram.com') >=0:
                data_dictionary['Instagram'] = sml

            elif sml.find('twitter.com') >=0:
                data_dictionary['Twitter'] = sml

            elif sml.find('linkedin.com') >=0:
                data_dictionary['LinkedIn'] = sml

            elif sml.find('tiktok.com') >=0:
                data_dictionary['TikTok'] = sml 

    # return social_media_links
    # return list(set(social_media_links))

def write_data_in_file(list_of_dictionaries,count):

    """
    write data in csv file...
    """
    csv_column = ['Shopify Store Website','Email','Facebook Page','Twitter','LinkedIn','TikTok','Instagram']

    with open('data.csv', 'a+', newline='',encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=csv_column)
        if count == 0:
            dict_writer.writeheader()
        dict_writer.writerows(list_of_dictionaries)


if __name__ == "__main__":

    # Read data from JSON file...

    global data_dictionary 

    json_dict = read_data_from_json()
    urls = read_urls_()
    offset = 0

    for url in urls:
        template_list = []
        data_dictionary = {'Shopify Store Website' : 'NaN','Email' : 'NaN', 'Facebook Page' : 'NaN', 'Twitter' : 'NaN',
        'LinkedIn' : 'NaN', 'TikTok' : 'NaN', 'Instagram' : 'NaN'}

        data_dictionary['Shopify Store Website'] = url

        shopify_store_link = url.strip()
        r = requests.get(shopify_store_link)

        if r.status_code == 200:

            # if the webpage redirect request status code as 200
            # then scraping will be done through HTTP request

            try:
                links = []
                soup = BeautifulSoup(r.content, 'html.parser')
                for link in soup.findAll('a'):
                    links.append(link.get('href'))

                # a for loop block to iterate the scraped links one by one...

                extract_social_media_links(links)
                contact_page = get_contact_us_page(shopify_store_link,links)
                extract_email(url,contact_page,200)

            except Exception:
                pass

        else:

            # if the webpage redirect request status code which is not 200
            # then scraping will be done through Selenium Google driver

            driver = start_web_driver(chromedriver_path)
            driver.get(url)
            source_code = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

            try:

                soup = BeautifulSoup(source_code, 'html.parser')
                links = []
                for link in soup.findAll('a'):
                    links.append(link.get('href'))

                # a for loop block to iterate the scraped links one by one...

                social_media_urls = extract_social_media_links(links)
                contact_page = get_contact_us_page(shopify_store_link,links)
                extract_email(url,contact_page,1)

            except Exception:
                pass
        
        template_list.append(data_dictionary)
        write_data_in_file(template_list,offset)
        print("Scraped Data is {}".format(data_dictionary))
        offset += 1
