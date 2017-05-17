import re

class ParseCredentialFile(object):
	
	def __init__(self, filename):
		self.dictionary = {}
		
		f = open(filename)
		self.dictionary = dict([line.split() for line in f])
						
		f.close()
		
	def get_username(self):
		return self.dictionary.get("username")
	
	def get_password(self):
		return self.dictionary.get("password")