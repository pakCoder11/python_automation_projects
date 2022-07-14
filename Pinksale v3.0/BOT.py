# ================================
# Pinksale Multi-Threaded Bot

# ================================

import threading
from selenium import webdriver
import time
import pyautogui
from screen_search import *
import json


def wait_until_appear(png_image):
    """
    This function is used to wait until the HTML element appears on the screen
    """

    while(True): 
        if len(LocateImageOnScreen(png_image)) > 0: 
            break
        else: 
            time.sleep(0.5)

def read_data_from_json():
    """
    Read data from JSON file...
    """
    with open('data.json') as f:
        data = json.load(f)

    return data

def click_on_token_addresses(token_image,driver):
    """
    This function is used to click on Token addresses
    """
    # Pressup_keyboard(30)

    while(True): 
        Pressdown_keyboard(5)
        time.sleep(2)

        if len(LocateImageOnScreen(token_image)) > 0: 
            _img_x_y = LocateImageOnScreen(token_image)

            try:
                # time.sleep(2)       
                pyautogui.click(_img_x_y[0]+500,_img_x_y[1],clicks=1) # (x,y) 
                driver.switch_to.window(driver.window_handles[0])

            except IndexError:
                pass
 
            break
            # end the loop

def auto_bot(driver):    

    driver.maximize_window()
    
    # wait_until_appear('website_icon.png')
    time.sleep(3)
    ClickImageOnScreen('connect.png',0,50,1)
    time.sleep(1)

    # image_png,_x,_y,total_clicks  
    ClickImageOnScreen('WEBSITE.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])

    ClickImageOnScreen('TWITTER.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])

    # click_on_back_link()
    
    ClickImageOnScreen('FACEBOOK.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])
    # click_on_back_link()

    ClickImageOnScreen('INSTAGRAM.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    # click_on_back_link()
    driver.switch_to.window(driver.window_handles[0])

    ClickImageOnScreen('TELEGRAM.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])

    # click_on_back_link()

    ClickImageOnScreen('GITHUB.png',2,2,1)
    time.sleep(1)
    # driver.get(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])


    ClickImageOnScreen('DISCORD.png',2,2,1)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])

    ClickImageOnScreen('REDDIT.png',3,3,1)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])


    click_on_token_addresses('PRESALE_ADDR.png',driver)
    click_on_token_addresses('TOKEN_ADDR.png',driver)

    # driver.execute_script("window.scrollTo(0,400)")
    # time.sleep(2)

    # presale_img_x_y = LocateImageOnScreen('PRESALE_ADDR.png')
    # token_address_x_y = LocateImageOnScreen('TOKEN_ADDR.png')

    # try:
    #     time.sleep(2)       
    #     pyautogui.click(presale_img_x_y[0]+500,presale_img_x_y[1],clicks=1) # (x,y) 
    #     driver.switch_to.window(driver.window_handles[0])
    #     # driver.get(driver.window_handles[0])

    # except IndexError:
    #     pass

    # try:
    #     time.sleep(2)
    #     # _x_y = LocateImageOnScreen('token_address_text.png')
    #     pyautogui.click(token_address_x_y[0]+500,token_address_x_y[1],clicks=1) # (x,y) 
    #     driver.switch_to.window(driver.window_handles[0])


    # except IndexError:
    #     pass

    time.sleep(2)
    scroll_up_and_down()

    driver.quit()

def Pressdown_keyboard(number_of_press_down):

    # this function is used to press the 'Down' key from keyboard automatically        
    for i in range(0,number_of_press_down):
        pyautogui.press('down')

def Pressup_keyboard(number_of_press_down):

    # this function is used to press the 'Down' key from keyboard automatically        
    for i in range(0,number_of_press_down):
        pyautogui.press('up')

def scroll_up_and_down():

    count = 0
    while(True):
        time.sleep(1)
        Pressdown_keyboard(15)
        count += 1

        if count == 4:
            break

    Pressup_keyboard(5)
    time.sleep(2)



def LocateImageOnScreen(image_png):

    # this function is used to search the image on screen and returns the co-ordinates
    # time.sleep(4)

    if pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8) != None:
        cordinates = pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8)
        position = []
        position.append(cordinates[0])
        position.append(cordinates[1])
        return position
    else:
        return []


def logs_write_to_file(_message_string):
    """
    Logs write to file
    """
    with open("logs.txt",'a+') as file:
        file.write(_message_string+'\n')

def ClickImageOnScreen(image_png,_x,_y,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    if len(LocateImageOnScreen(image_png)) > 0:

        cordinates = pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8)
        pyautogui.click(cordinates[0]+_x,cordinates[1]+_y,clicks=total_clicks) # (x,y) 

    else:
        pass

def create_threads_for_browser(_n_threads,proxy_list,path):
    """
    This function is used to create browser instances for each list, for example 
    if N number of proxies/account 
    """
    threading_list = []

    for i in range(0,_n_threads):
        try:
            t = threading.Thread(target=make_browser,args=(proxy_list[i],path))
            t.start()
            threading_list.append(t)
        except IndexError:
            pass

    for i in range(0,len(threading_list)):
        threading_list[i].join()

def make_browser(proxy,driver_path):
    """
    This function is used to return the list of selenium browser objects...
    """

    # Add proxy code for selenium browser
    # Start browser in icognito mode---
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Chrome(executable_path=driver_path,options=chrome_options)
    driver.get(project_link)

    _message_string = 'Social media links clicked... proxy used {}'.format(proxy)
    logs_write_to_file(_message_string)
    browser_list_objects.append(driver)

    return browser_list_objects

def thread_task(lock,driver):
    """
    task for thread
    """
    lock.acquire()
    auto_bot(driver)
    lock.release()

def read_proxies():
    """
    This function is used to read the proxies from the list...
    """
    proxy_list = []
    with open("proxies.txt","r") as file:
        data = file.readlines()

    for d in data:
        _string = d 
        _string = _string.replace('\n','')
        proxy_list.append(_string)

    return proxy_list


def read_proxies():
    """
    This function is used to read the proxies from the list...
    """
    proxy_list = []
    with open("proxies.txt","r") as file:
        data = file.readlines()

    for d in data:
        _string = d 
        _string = _string.replace('\n','')
        proxy_list.append(_string)

    return proxy_list

def select_proxies(PROXIES,_int_var_per_thread,TOTAL_proxies):
    """
    This function is used to select proxies from the list, proxies will be selected according to total windows
    """

    proxies_data_lists = []
    y = 0
    z = _int_var_per_thread

    for i in range(0,TOTAL_proxies):
        proxy_list = []
        for j in range(y,z):
            try:
                proxy_list.append(PROXIES[j])
            except IndexError:
                break
        if len(proxy_list) > 0:
            proxies_data_lists.append(proxy_list)

        y = z
        z += _int_var_per_thread


    return proxies_data_lists


def main_task(_drivers):
    """
    This function is used to initiate the main task
    """


    # creating a lock
    lock = threading.Lock()

    for x in range(0,len(_drivers)):
        t = threading.Thread(target=thread_task, args=(lock,_drivers[x]))
        # threads_list.append(t)
        t.start()
        t.join()

    # for t in threads_list:
    #   t.start()

    # for t in threads_list:
    #   t.join()

def check_error():
    """
    This function is used to identify the error on bot running...
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--proxy-server=%s' % proxy)

    driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)
    driver.get(project_link)
    driver.maximize_window()
    time.sleep(8)

    if len(LocateImageOnScreen('WEBSITE.png')) > 0:

        driver.quit()
        return False
    else:
        driver.quit()
        return True

# ============================================
# Main Function 
# Read DATA variables through JSON file including chromedriver path,total windows, project link
# Read proxies 
# Pass proxies to multi_task function to perform processing through synchronized multi-threadeding
# ============================================

if __name__ == "__main__":

    global browser_list_objects
    global project_link
    global chromedriver_path

    json_dict = read_data_from_json()
    project_link = json_dict["project_link"]
    chromedriver_path = json_dict["chromedriver_path"]
    windows_per_thread = int(json_dict["windows_per_thread"])

    if check_error() == False:

        data = read_proxies()
        _proxies_data = select_proxies(data,windows_per_thread,len(data))

        # Start Bot execution
        print("Bot is working perfectly in error-free environment...")
    
        i = 1
        for data in _proxies_data:
            try:
                browser_list_objects = []
                create_threads_for_browser(windows_per_thread,data,chromedriver_path)
                main_task(browser_list_objects)
                print("Bot Iteration number is {}".format(i))
            except IndexError:
                pass

            i += 1

    else:
        # if error appears then never initiate a driver
        print("Dear User, Bot is facing error IMAGE_RECOGNITION_ERROR_1101 due to improper detection of images - You need to watch the video error_fixing.mp4 to fix errors of Image Recognition Problem")
        