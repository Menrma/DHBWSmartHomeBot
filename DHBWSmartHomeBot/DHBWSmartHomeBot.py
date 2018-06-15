
import requests
import json
import time

from DialogManager import DialogManager

# Global variable for token
TOKEN = ""
# Global variable for URL
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

DM = DialogManager()

# Method for downloading content from url
def get_url_content(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content
	
# Method to transfer the url response to json
def get_json_from_url_content(url):
	content = get_url_content(url)
	jsonContent = json.loads(content)
	return jsonContent

# Method for getting updates
def get_updates(offset=None):
	url = URL + "getupdates?timeout=100"
	if offset:
		url += "&offset={}".format(offset)
	jsonContent = get_json_from_url_content(url)
	return jsonContent

## Method to get last chatd id and text
#def get_last_chat_id_and_text(update_result):
#	number_updates = len(update_result["result"])
#	last_update = number_updates - 1
#	chat_id = update_result["result"][last_update]["message"]["chat"]["id"]
#	text = update_result["result"][last_update]["message"]["text"]
#	return (chat_id, text)

# Method for sendig a message
def send_message(chat_id, text):
	url = URL + "sendMessage?chat_id={}&text={}".format(chat_id, text)
	get_url_content(url)

# Method for getting message offset
def get_offset(updates):
	update_length = len(updates["result"])
	last_update = update_length - 1
	offset = updates["result"][last_update]["update_id"]
	return offset

# Echo all users
def echo_all_users(currentUpdates):
	for update in currentUpdates["result"]:
		try:
			text = update["message"]["text"]
			chat_id = update["message"]["chat"]["id"]
			response = DM.executeMessage(text)
			send_message(chat_id, response)
			print("Message: {}, Chat Id:{}".format(text, chat_id))
		except Exception as e:
			print(e)

## Main method
#def main():
#	last_chat = (None, None)
#	while True:
#		currentUpdates = get_updates()
#		chat_id, text = get_last_chat_id_and_text(currentUpdates)
#		if(chat_id, text) != last_chat:
#			send_message(chat_id, text)
#			print("Message: {}, Chat Id:{}".format(text, chat_id))
#			last_chat = (chat_id, text)
#		time.sleep(1.0)

def main2():
	last_update_id = None
	while True:
		currentUpdates = get_updates(last_update_id)
		if len(currentUpdates["result"]) > 0:
			last_update_id = get_offset(currentUpdates) + 1
			echo_all_users(currentUpdates)
		time.sleep(1.0)

# Entry point of the application
if __name__ == "__main__":
	main2()
	#messages = ["Schalte das Licht in der Küche ein", "Licht in der Küche ein", "Ist das Licht in der Küche an?", 
	#		 "Was zeigt der Feuchtigkeitsmesser an?", "Was zeigt der Sensor in der Küche an?", "Wie ist die Steckdose in der Küche?", "Licht in der Küche?", "Steckdose an?",
	#		 "Licht in der Küche ein", "Licht an", "Schalte in der Küche das Licht ein"]

	#messages2 = ["Was zeigt der Sensor in der Küche an?", "Wie ist die Steckdose in der Küche?"]
	##["Was zeigt der Feuchtigkeitsmesser an?", "Bad"]
			  

	#dm = DialogManager()

	#while True:
	#	print("Eingabe: ")
	#	eingabe = input()
	#	if eingabe == "exit":
	#		print("Goodbye :-)")
	#		break
	#	resonse = dm.executeMessage(eingabe)

	#dm.executeMessage("Licht an")
	#dm.executeMessage("Wohnzimmer")

	#for message in messages2:
	#	dm.executeMessage(message)