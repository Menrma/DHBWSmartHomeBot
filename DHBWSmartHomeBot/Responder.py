class Responder(object):
	""" Class for generating an answer based on given informations """

	def __init__(self):
		self.__message = ""
		self.__frame = None


	def GenerateResponse(self, frame):
		# check if frame is complete
		self.__frame = frame
		
		if not self.__frame.ItemInRoom and self.__frame.Item and self.__frame.Room:
			return self.__choosenItemNotInRoom()
		elif not self.__frame.IsComplete:
			return self.__parsedMessageNotComplete()
		else:
			return self.__messageOkay()


	def __parsedMessageNotComplete(self):
		self.__frame.FurtherInformationRequired = True
		if self.__frame.IsQuestion:
			# for question relevant: room and item
			if not self.__frame.Room:
				return "In welchem Raum?"
			elif not self.__frame.Item:
				return "Um welchen Gegenstand handelt es sich?"
		else:
			# relevant: room, item and state
			if not self.__frame.Room:
				return "Um welchen Raum handelt es sich?"
			elif not self.__frame.Item:
				return "Um welchen Gegenstand handelt es sich?"
			elif not self.__frame.State:
				return "Wie ist der Status des Gegenstand?"

	def __choosenItemNotInRoom(self):
		self.__frame.FurtherInformationRequired = False
		return "Der Gegenstand {} befindet sich nicht in Raum {}".format(self.__frame.Item.title(), self.__frame.Room.title())

	def __messageOkay(self):
		self.__frame.FurtherInformationRequired = False
		answer = ""
		bezeichner = ""

		# TEST
		if not self.__frame.State:
			self.__frame.State = "<STATE>"

		if self.__frame.RoomArticle:
			answer = "{} in {} {} ist {}".format(self.__frame.Item.title(), self.__frame.RoomArticle, self.__frame.Room.title(), self.__frame.State)
		else:
			room = ''.join(self.__frame.Room)
			if room == "küche":
				bezeichner = "in"
			else:
				bezeichner = "im"
			answer = "{} {} {} ist {}".format(self.__frame.Item.title(), bezeichner, self.__frame.Room.title(), self.__frame.State)
		
		answer = answer.strip()
		return answer