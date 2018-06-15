class Frame(object):
	""" Frame class for storing extracted informations """
    
	def __init__(self):
		self.__fullMessage = ""
		self.__room = ""
		self.__roomArticle = ""
		self.__item = ""
		self.__state = ""
		self.__isComplete = False
		self.__itemInRoom = False
		self.__isQuestion = False
		self.__furtherInformationRequired = False

	@property
	def FullMessage(self):
		return self.__fullMessage

	@FullMessage.setter
	def FullMessage(self, value):
		self.__fullMessage = value

	@property
	def Room(self):
		return self.__room

	@Room.setter
	def Room(self, value):
		self.__room = value

	@property
	def RoomArticle(self):
		return self.__roomArticle

	@RoomArticle.setter
	def RoomArticle(self, value):
		self.__roomArticle = value

	@property
	def Item(self):
		return self.__item

	@Item.setter
	def Item(self, value):
		self.__item = value

	@property
	def State(self):
		return self.__state

	@State.setter
	def State(self, value):
		self.__state = value
	@property
	def IsComplete(self):
		return self.__isComplete

	@IsComplete.setter
	def IsComplete(self, value):
		self.__isComplete = value

	@property
	def ItemInRoom(self):
		return self.__itemInRoom

	@ItemInRoom.setter
	def ItemInRoom(self, value):
		self.__itemInRoom = value

	@property
	def IsQuestion(self):
		return self.__isQuestion

	@IsQuestion.setter
	def IsQuestion(self, value):
		self.__isQuestion = value

	@property
	def FurtherInfomrationRequired(self):
		return self.__furtherInformationRequired

	@FurtherInfomrationRequired.setter
	def FurtherInformationRequired(self, value):
		self.__furtherInformationRequired = value