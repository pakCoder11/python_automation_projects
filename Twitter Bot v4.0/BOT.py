# ------------------------------------
# libraries required for bot running
# --------------------------------------

import csv
from os import error, path
from selenium import webdriver
import re
import time
import pyautogui
from pyautogui import *
import pandas as pd
import random
import json
# ----------------------------------

def Pressdown_keyboard(number_of_press_down):

    # this function is used to press the 'Down' key from keyboard automatically        
    for i in range(0,number_of_press_down):
        pyautogui.press('down')

def PressUp_keyboard(number_of_press_down):

    # this function is used to press the 'Down' key from keyboard automatically        
    for i in range(0,number_of_press_down):
        pyautogui.press('up')

def moveCursorAtTop():
    """
    This function is used to place the cursor at the right top of the screen...
    """

    if LocateImageOnScreen('twt_twitter_logo.png') == True:

        cordinates = pyautogui.locateOnScreen('twt_twitter_logo.png')
        pyautogui.click(cordinates[0]+120,cordinates[1]+10,clicks=1)

        # pos = search.imagesearch()
        # pyautogui.click(pos[0]+50,pos[1],clicks=1) # (x,y) 

def convert_dataframe_into_array(_df):
    _list_ = _df.tolist()
    return _list_


def load_comments(): 
    """
    This function is used to load the comments from comments.txt

    """
    with open("comments.txt","r") as file: 
        data = file.readlines() 

    comments_list = []
    for d in data: 
        string = str(d)
        string = string.replace('\n','')
        comments_list.append(string)

    return comments_list

def ClickImageOnScreen(image_png,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    cordinates = pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8)
    pyautogui.click(cordinates[0]+5,cordinates[1]+5,clicks=total_clicks)

def LocateImageOnScreen(image_png):

    # this function is used to search the image on screen and returns the co-ordinates
    # time.sleep(4)

    if pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8) != None:
        return True

    else:
        return False

# Method to read data from JSON file 
def read_data_from_json():
    """
    Read data from JSON file...
    """
    with open('data.json') as f:
        data = json.load(f)

    return data

def locate_when_appear(png_image):
    """
    This function is used to find image when it appears...
    It prevents the unwanted time sleeps
    """
    while(True): 
        if LocateImageOnScreen(png_image) == True: 
            break
        else: 
            time.sleep(0.5)

def click_when_appear(png_image):
    """
    This function is used to click on image when it appears...
    It prevents the unwanted time sleeps
    """

    while(True): 
        if LocateImageOnScreen(png_image) == True: 
            ClickImageOnScreen(png_image,1)
            break
        else: 
            time.sleep(0.5)

def type_hashtag_on_search_bar(): 
    """
    This function is used to type the hashtags
    """
    _hashtag = read_hashtag_from_file() 
    time.sleep(3)
    click_when_appear('twt_explore.png')
    time.sleep(3)
    click_when_appear('twt_search_bar.png')
    pyautogui.write(_hashtag)
    pyautogui.press('enter')
    time.sleep(3)
    _log_string = 'Twitter Hashtag used  : {} '.format(_hashtag)                    
    write_to_log_file(_log_string)

def read_hashtag_from_file(): 
    """
    This function is used to read the hashtags from the hashtags.txt
    """

    with open("hashtag.txt","r") as file:
        data = file.readlines()

    if len(data) == 1:
        string = str(data[0])
        string = string.replace('\n','')
        return string
    else: 
        # select random hashtags from the list... 
        _r_string = str(random.choice(data))
        _r_string = _r_string.replace('\n','')
        return _r_string

def auto_login(username,password): 
    """
    This function is used to login in to twitter account
    """
    # driver.get('https://twitter.com/')
    # time.sleep(3)
    # if len(LocateImageOnScreen('twt_Login.png')) == 0: 

    # click_when_appear('twt_twitter__logo.png')
    # Pressdown_keyboard(5)
    # click_when_appear('twt_signin.png')

    click_when_appear('twt_username_field.png')
    pyautogui.write(username)
    pyautogui.press('enter')
    time.sleep(2)
    # click_when_appear('twt_password.png')
    # time.sleep(2)
    pyautogui.write(password)
    pyautogui.press('enter')
    type_hashtag_on_search_bar()
    # time.sleep(2)
    click_when_appear('twt_latest_tweets_links.png')
    time.sleep(3)

        # return 1
    # else:
        # return 0

def write_to_log_file(_log_string): 
    """
    This function is used to write details of commenting into log file...
    """
    with open("logs.txt",'a+') as log_file:
        log_file.write(_log_string+'\n')

def discard_tweet(): 

    """
    This function is used to discard the tweet, if reply button wasn't appear on screen
    """

    if LocateImageOnScreen('twt_pre_reply_btn.png') == False:
        # Close the tweet reply windowWillpower123

        click_when_appear('twt_cancel_btn.png')

        return True
    else:
        return False

def scrolling_up_and_down(n):

    time.sleep(3)
    Pressdown_keyboard(n)
    PressUp_keyboard(n)

def retweet():
    if LocateImageOnScreen('twt_retweet.png') == True: 

        ClickImageOnScreen('twt_retweet.png',1)
        time.sleep(1)
        ClickImageOnScreen('twt_retweet_text.png',1)

def click_on_scroll_button(): 

    # This function is used to click on scroll button when it's appear to hide Reply button

    if LocateImageOnScreen('scroll.png') == True:        
        cordinates = pyautogui.locateOnScreen('scroll.png', grayscale=True, confidence=0.8)
        pyautogui.click(cordinates[0]+9,cordinates[1]+9,clicks=2)
        time.sleep(1)
        pyautogui.click(cordinates[0]+9,cordinates[1]+9,clicks=2)


def auto_comment(comments,twitter_username,_limit): 
    """
    This functionm is used to type the auto-comments until the limit was reached...
    """
    counter = 0
    
    locate_when_appear('three_dots.png')
    scrolling_up_and_down(250)
    
    while(True):

        if LocateImageOnScreen('twt_comment_btn.png') == True:

            try:
                # an exception if failed to click on comment button...

                if like_tweet_flag == "True": 
                    ClickImageOnScreen('twt_like.png',1)
                    time.sleep(1)

                if retweet_flag == "True": 
                    retweet()
                    time.sleep(3)

                ClickImageOnScreen('twt_comment_btn.png',1)
                time.sleep(2)

                if discard_tweet() == False:

                    _comment_string = random.choice(comments)
                    pyautogui.write(_comment_string)
                    time.sleep(2)
                    pyautogui.press('space') 
                    time.sleep(2)
                    click_on_scroll_button()
                    # if the reply button wasn't appear then it means user has to discard the tweet

                    click_when_appear('twt_reply_btn.png')                         
                    time.sleep(5)
                    _log_string = 'ID : {} Twitter username : {}, Comment : {} '.format(counter+1,twitter_username,_comment_string)                    
                    moveCursorAtTop()
                    counter += 1 
                    write_to_log_file(_log_string)

                    print("Auto-comment by bot is ",_comment_string)
                    print("Data write to log file...")

                    if counter == 20:
                        scrolling_up_and_down(50)

                    if counter == _limit: 
                        break
                    Pressdown_keyboard(15)

                else: 
                    Pressdown_keyboard(20)

            except TypeError:
                Pressdown_keyboard(5)
                
        else:

            moveCursorAtTop()
            time.sleep(2)
            Pressdown_keyboard(8)
            time.sleep(2)



if __name__ == "__main__":
    # Main body of the function....

    global  like_tweet_flag, retweet_flag
    json_dict = read_data_from_json()
    chromedriver_path = json_dict["chromedriver_path"]
    TOTAL_COMMENTS_LIMIT = int(json_dict["comments_limit"])

    retweet_flag = json_dict["retweet"]
    like_tweet_flag = json_dict["like"]

    # accounts_file = json_dict["accounts_data_file"]
    # comments_file = json_dict["comments_data_file"]
    # hashtags_file = json_dict["hashtags_data_file"]


    df = pd.read_csv('accounts.csv')
    _users = convert_dataframe_into_array(df['username'])
    _passwords = convert_dataframe_into_array(df['password'])

    # Auto comment
    comments_array = load_comments()    
    print("Comments are loaded... total comments are ",len(comments_array))

    # ----------------------
    # NEW CODE BLOCK
    # ----------------------

    for i in range(0,len(_users)): #iterate twitter accounts one by one...

        try:

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)
            driver.maximize_window()
            driver.get('https://twitter.com/home')

            auto_login(_users[i],_passwords[i])
            auto_comment(comments_array, _users[i],TOTAL_COMMENTS_LIMIT)
            time.sleep(2)
            driver.quit()

        except IndexError:
            pass
            



    # if LocateImageOnScreen('hash.png') == True:
        # ClickImageOnScreen('hash.png',1)
    # print(bool_flag)
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--incognito")
    # driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)
    # driver.maximize_window()
    # driver.get('https://twitter.com/home')
    # driver.quit()


