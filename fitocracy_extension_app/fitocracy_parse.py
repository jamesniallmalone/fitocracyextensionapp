import json
import re
import os

import cookielib
import urllib2
import urllib 

from fitocracy_rest_api import *

class FitocracyParserSession(object):
	def __init__(self, opener):
		self.__restsession = FitocracyRestApi(opener)
		self._store_userinfo()

	def _store_userinfo(self):
		content = self.__restsession.get_profile()
		
		self.__user_id = re.search("""var user_id = "(.+?)";""",content).group(1)
		self.__username = re.search("""var username = "(.+?)";""",content).group(1)
		
		self.__previousworkoutdirectory = 'previousruns/{0}'.format(self.__user_id)
		
		if not os.path.exists(self.__previousworkoutdirectory):
			os.makedirs(self.__previousworkoutdirectory)
		
	def get_user_id(self):
		return self.__user_id
	
	def get_username(self):
		return self.__username
		
	def get_full_activity_history(self, id):
		return self.__restsession.getUniqueActivity(id) if type(id) is int else False
	
	def get_user_points(self):
		return self.__restsession.getUserPoints(self.__username)
			
	def get_user_activities(self):
		return self.__restsession.getUserActivities(self.__user_id)
	'''	
	def update_current_workout(self):
		uactivites_tojson = self.get_user_activities()
		print(uactivites_tojson)
		currentworkout = json.loads(uactivites_tojson)
		if self._check_new_workout(currentworkout) == True:
			print("New workout found.")
			self._outputdirectory(self.__previousworkoutdirectory + '/previous_workout_summary.txt', currentworkout)
			print("Output to directory")
		else:
			print('No new workout.')
				
	def _find_json_diffs(self, jsona, jsonb):
		listofdiffids = []
		
		for x_key in jsona:
			if x_key not in jsonb:
				listofdiffids.append(x_key["id"])
			elif jsona[x_key] != jsonb[x_key]:
				listofdiffids.append(x_key["id"])
				
		print listofdiffids
		return listofdiffids
		
		
	def _check_new_workout(self, currentworkout):
		if not os.path.exists(self.__previousworkoutfile):
			return True
		
		with open(self.__previousworkoutfile, 'r') as myfile:
			data = json.loads(myfile.read())
			
		if len(self._find_json_diffs(currentworkout, data)) > 0:
			return True
			
		return False
			
	def _outputdirectory(self, directory, filecontent):
		outputfile = open(directory, "w+")
		outputfile.write(filecontent)
		outputfile.close()
	'''