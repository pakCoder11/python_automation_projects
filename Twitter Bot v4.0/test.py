import pyautogui
import time

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

def click_on_scroll_button(): 

    # This function is used to click on scroll button when it's appear to hide Reply button

    if LocateImageOnScreen('scroll.png') == True:        
        cordinates = pyautogui.locateOnScreen('scroll.png', grayscale=True, confidence=0.8)
        pyautogui.click(cordinates[0]+9,cordinates[1]+9,clicks=2)

if __name__ == "__main__":

    time.sleep(3)
    flag =  click_on_scroll_button()
    print(flag)

