
import re
from Frame import Frame

PATTERN = [[r'((\w*)\s(der|die|das){0,1}\s){0,1}(\w*)(\s(\w*)\s){0,1}(\w*\s){0,1}([A-Za-zäöüÄÖÜ]*)\s(ein|an|aus){1}(\.|\!| ){0,1}$', "S"],
			[r'(ist|was|wie){1}\s(\w*\s){0,1}(der|die|das){0,1}\s(\w*){0,1}\s((in|im){0,1}\s(der|die|das){0,1}\s([A-Za-zäöüÄÖÜ]*)){0,1}\s(an|aus|ein){0,1}(\?){0,1}$',"Q"],
			[r'(ist|was|wie){1}\s(\w*\s){0,1}(der|die|das){0,1}\s(\w*){0,1}\s(an|aus|ein){0,1}(\?){0,1}$', "Q"],
			[r'^(\w*){0,1}\s(in|im)(\s(der\s|die\s|das\s){0,1})([A-Za-zäöüÄÖÜ]*)(\?){1}$', "Q"],
			[r'^(\w*)\s(an|ein|aus)(\?)$', "Q"]]

ARTICLES = ['der', 'die', 'das']

ROOMS = ["küche", "bad", "wohnzimmer"]

ITEM = ["licht", "ofen", "musik", "feuchtigkeitsmesser", "sensor"]

ROOM_ITEM = [["küche", ["licht", "ofen", "sensor"]],
		  ["bad", ["licht", "feuchtigkeitsmesser"]],
		  ["wohnzimmer",["licht", "musik"]]]

class Parser(object):
	""" Class for extracting informations of the message and filling the frame """

	def __init__(self):
		self.__message = ""
		self.__frame = None

	def parseMessage(self, message):
		# lowercase the current message
		self.__message = message.lower()
		if(self.__frame == None or not self.__frame.FurtherInformationRequired):
			self.__parseNewMessage()
		elif self.__frame.FurtherInformationRequired:
			self.__parseFurtherInformation()

		return self.__frame

	def __parseNewMessage(self):
		self.__frame = Frame()
		match = self.__checkPattern()
		
		if match:
			matches = self.__convertMatch(match)
			# check room and write to frame
			self.__checkRoomAndWriteToFrame(matches)

			## check room and item
			#room, article = self.__checkRoomInMessage(matches)
			## write room and article to frame
			#self.__frame.Room = room
			#self.__frame.RoomArticle = article

			self.__checkItemAndWriteToFrame(matches)

			#item = self.__checkItemInMessage(matches)
			## write item to frame
			#self.__frame.Item = item

			if not self.__frame.IsQuestion:
				if matches[len(matches)-1] in [".", "!"]:
					state = matches[len(matches)-2]
				else:
					state = matches[len(matches)-1]
				# write state to frame
				self.__frame.State = state

			# Check if item is in room
			self.__checkItemInRoomAndWriteToFrame(self.__frame.Room, self.__frame.Item)
			
			#if room and item:
			#	itemInRoom = self.__checkItemInRoom(room, item)
			#	# write result to frame
			#	self.__frame.ItemInRoom = itemInRoom
		else:
			self.__frame = None
			print("Pattern not found. Message: {}".format(self.__message))

		# in both cases: return frame to caller class
		return self.__frame

	def __parseFurtherInformation(self):
		# checking further informations in case of room or item or state is missing
		message = self.__message.split(" ")
		if not self.__frame.Room:
			# check room and write to frame
			self.__checkRoomAndWriteToFrame(message)

			#room, article = self.__checkRoomInMessage(message)
			## write room and article to frame
			#self.__frame.Room = room
			#self.__frame.RoomArticle = article
		elif not self.__frame.Item:
			#items = self.__frame.Item.split(" ")
			self.__checkItemAndWriteToFrame(message)

			#item = self.__checkItemInMessage()
			## write state to frame
			#self.__frame.State = state
		elif not self.__frame.IsQuestion and not self.__frame.State:
			if state in ["an", "ein", "aus"]:
				# write state to frame
				self.__frame.State = self.__state

		# Check if item is in room
		self.__checkItemInRoomAndWriteToFrame(self.__frame.Room, self.__frame.Item)

		#if self.__frame.Room and self.__frame.Item:
		#	itemInRoom = self.__checkItemInRoom(self.__frame.Room, self.__frame.Item)
		#	# write result to frame
		#	self.__frame.ItemInRoom = itemInRoom
		return self.__frame

	def __checkPattern(self):
		match = None
		# loop on all given patterns
		for (pattern, type) in PATTERN:
			match = re.findall(pattern, self.__message)
			
			if match:
				# check if matched by a question or statement
				# else block not necessary because 'false' is default in frame class
				if type == "Q":
					self.__frame.IsQuestion = True
				break
		return match

	def __convertMatch(self, match):
		matches = []
		for entry in match[0]:
				if entry:
					matches.append(entry)
		return matches

	def __checkRoomAndWriteToFrame(self, match):
			# check if room is in message
			room, article = self.__checkRoomInMessage(match)
			# write room and article to frame
			self.__frame.Room = room
			self.__frame.RoomArticle = article

	def __checkRoomInMessage(self, match):
		# check room in message
		article = None
		rooomFound = set(ROOMS) & set(match)
		if rooomFound:
			rooomFound = next(iter(rooomFound))
			article = self.__checkArticleBeforeRoom(match, rooomFound)
		else:
			rooomFound = None
		return (rooomFound, article)

	def __checkArticleBeforeRoom(self, match, room):
		index = match.index(room)
		article = match[index-1].rstrip()
		if article not in ARTICLES:
			article = None
		return article

	def __checkItemAndWriteToFrame(self, match):
		# check if item is in message	
		item = self.__checkItemInMessage(match)
		# write item to frame
		self.__frame.Item = item

	def __checkItemInMessage(self, match):
		# check item in message
		itemFound = set(ITEM) & set(match)
		if itemFound:
			itemFound = next(iter(itemFound))
		else:
			itemFound = None
		return itemFound

	def __checkItemInRoomAndWriteToFrame(self, room, item):
		# Check if item is in room
		if room and item:
			itemInRoom = self.__checkItemInRoom(room, item)
			# write result to frame
			self.__frame.ItemInRoom = itemInRoom

	def __checkItemInRoom(self, room, item):
		for value in ROOM_ITEM:
			if value[0] == room:
				for items in value[1]:
					if items == item:
						return True
		return False