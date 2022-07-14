import pyautogui 
from screen_search import *
import time 
import pandas as pd

def ClickImageOnScreen(image_png,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    search = Search(image_png)
    pos = search.imagesearch()
    # pyautogui.moveTo(pos[0]+10,pos[1])
    pyautogui.click(pos[0],pos[1],clicks=total_clicks) # (x,y) 

def LocateImageOnScreen(image_png):
    # this function is used to search the image on screen and returns the co-ordinates

    # time.sleep(4)
    search = Search(image_png)
    pos = search.imagesearch()

    if pos[0] != -1:
        # pyautogui.moveTo(pos[0], pos[1])
        return pos
    else:
        return []

def type_backspace():
	"""
	Type backspace...
	"""
	for i in range(0,50):
		pyautogui.press('backspace')

def auto_message_send(dataframe):

	"""
	This function is used to send auto-messages to whatsapp users one by one...
	"""

	contacts = df['contacts']
	messages = df['messages']

	for i in range(0,len(messages)):

		ClickImageOnScreen('search.png',1)
		time.sleep(2)

		pyautogui.write(contacts[i])
		time.sleep(2)

		if len(LocateImageOnScreen('chats.png')) > 0 or len(LocateImageOnScreen('contacts.png')) > 0 or len(LocateImageOnScreen('groups.png')) > 0 or len(LocateImageOnScreen('messages.png')) > 0:

			pyautogui.press('enter')
			time.sleep(1)
			pyautogui.write(messages[i])
			pyautogui.press('enter')
			time.sleep(3)
		else:
			type_backspace() 


if __name__ == "__main__":
	df = pd.read_csv('info.csv')
	print("Contacts are loaded...")
	time.sleep(5)
	auto_message_send(df)
