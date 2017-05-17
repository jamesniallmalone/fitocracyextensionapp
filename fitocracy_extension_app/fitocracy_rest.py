import json
import re

import cookielib
import urllib2
import urllib 

class FitocracyRestSession(object):
	def __init__(self):
		self.__BASE_URL = "https://www.fitocracy.com"
		self.__cookie_jar = cookielib.CookieJar()
		self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie_jar))
		self.__user_id = False
		self.__logged_in = False
		self.__username = False
		
	def _rest_request(self, path):
		response = self.__opener.open(self.__BASE_URL + path)
		return str(response.read())
		
	def login(self, user, password):
		login_url = self.__BASE_URL +"/accounts/login/"
		self.__opener.open(login_url)
		
		csrf = [cookie.value for cookie in self.__cookie_jar if cookie.name == "csrftoken"][0]
				
		post_data = bytes(urllib.urlencode({'username': user,
									 'password': password,
									 'csrfmiddlewaretoken': csrf,
									 'login': 'Log In',
									 'next': ''}))
		
		headers = {"Referer": "https://www.fitocracy.com/accounts/login/",
				  "Origin": "https://www.fitocracy.com"}
		
		request = urllib2.Request(login_url, post_data, headers=headers)
		response = self.__opener.open(request)
		
		content = str(response.read())
		
		self.__logged_in = False if "Something went wrong.<br />Please try again later." in content else True
		self.store_userinfo()
		
		return self.__logged_in
		
	def store_userinfo(self):
		if self.__logged_in == False:
			return
		
		content = self._rest_request("/profile")
		
		self.__user_id = re.search("""var user_id = "(.+?)";""",content).group(1)
		self.__username = re.search("""var username = "(.+?)";""",content).group(1)
		
	def get_user_id(self):
		return self.__user_id
	
	def get_username(self):
		return self.__username
		
	def get_full_activity_history(self, id):
		if self.__logged_in == False:
			return False
		
		if type(id) is int:
			return self._rest_request("/_get_activity_history_json/?activity-id={0}".format(id))
		else:
			return False
		
	def get_user_points(self):
		if self.__logged_in == False:
			return False
		
		return self._rest_request("/get-user-points/?user={0}".format(self.__username))
			
	def get_user_activities(self):
		if self.__logged_in == False:
			return False
		
		return self._rest_request("/get_user_activities/{0}".format(self.__user_id))
		