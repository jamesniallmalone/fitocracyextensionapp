import json
import re
import os

import cookielib
import urllib2
import urllib 

class FitocracyRestApi(object):
	
	def __init__(self, opener):
		self.__BASE_URL = "https://www.fitocracy.com"
		self.__opener = opener
		
	def _rest_request(self, path):
		response = self.__opener.open(self.__BASE_URL + path)
		return str(response.read())
	
	def get_profile(self):
		return self._rest_request("/profile")
	
	def getUniqueActivity(self, activityid):
		return self._rest_request("/_get_activity_history_json/?activity-id={0}".format(activityid))
	
	def getUserPoints(self, username):
		return self._rest_request("/get-user-points/?user={0}".format(username))
		
	def getUserActivities(self, userid):
		return self._rest_request("/get_user_activities/{0}".format(userid))