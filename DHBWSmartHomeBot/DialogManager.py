
from Parser import Parser
from Frame import Frame
from Responder import Responder

class DialogManager(object):
	""" Dialog Manager class for interacting with other Dialog-Layer classes """
 
	def __init__(self):
		self.__message = ""
		self.__parser = Parser()
		self.__frame = None
		self.__responder = Responder()

	def executeMessage(self, message):
		response = ""
		print("Bearbeite Nachricht: {}".format(message))
		self.__message = message
		self.__callParser()
		if self.__frame:
			self.__frame.FullMessage = message
			self.__checkFrameComplete()
			self.__printFrame(self.__frame)

			if self.__frame.IsComplete:
				# frame is complete
				print("FRAME IS COMPLETE")
				# call action stage
				print("CALL ACTION STAGE")
				# call responder for generating an answer
				print("CALL RESPONDER")
				response = self.__responder.GenerateResponse(self.__frame)
			else:
				# frame is incomplete
				print("FRAME IS INCOMPLETE")
				# call responder
				print("CALL RESPONDER")
				response = self.__responder.GenerateResponse(self.__frame)

			if response == None:
				response = "Ich habe Sie leider nicht verstanden."

			print("Antwort: {}\n\n".format(response))
		else:
			# something went wrong with the frame
			response = "Ich habe Sie leider nicht verstanden."
			print("Antwort: Ich habe Sie leider nicht verstanden.\n\n")

		return response

	def __callParser(self):
		self.__frame = self.__parser.parseMessage(self.__message)

	def __checkFrameComplete(self):
		if self.__frame.Room and self.__frame.Item:
			if not self.__frame.IsQuestion and self.__frame.State or self.__frame.IsQuestion:
				#if self.__frame.ItemInRoom:
				self.__frame.IsComplete = True
				#else:
				#	self.__frame.IsComplete = False
			else:
				self.__frame.IsComplete = False
		else:
			self.__frame.IsComplete = False
		
	# TEST
	def __printFrame(self, frame):
		print("Room: {}, Article: {}, Item: {}, State: {}, IsQuestion: {}, ItemInRoom: {}, IsComplete: {}".format(frame.Room, frame.RoomArticle, frame.Item, frame.State, frame.IsQuestion, frame.ItemInRoom, frame.IsComplete))