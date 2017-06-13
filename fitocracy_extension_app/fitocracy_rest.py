import json
import re
import os

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
		
		headers = {"Referer": login_url,
				  "Origin": self.__BASE_URL}
		
		request = urllib2.Request(login_url, post_data, headers=headers)
		response = self.__opener.open(request)
				
		content = str(response.read())
		
		self.__logged_in = False if "<!-- end of login modal -->" in content else True
		self._store_userinfo()
		
		return self.__logged_in
		
	def _store_userinfo(self):
		if self.__logged_in == False:
			return
		
		content = self._rest_request("/profile")
		
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
		if self.__logged_in == False:
			return False
		
		if type(id) is int:
			return self._rest_request("/_get_activity_history_json/?activity-id={0}".format(id))
		else:
			return False
		
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
		if self.__logged_in == False:
			return False
		
		if not os.path.exists(self.__previousworkoutfile):
			return True
		
		with open(self.__previousworkoutfile, 'r') as myfile:
			data = json.loads(myfile.read())#.replace('\n','')
			
		if len(self._find_json_diffs(currentworkout, data)) > 0:
			return True
			
		return False
			
	def _outputdirectory(self, directory, filecontent):
		outputfile = open(directory, "w+")
		outputfile.write(filecontent)
		outputfile.close()
		
	def get_user_points(self):
		if self.__logged_in == False:
			return False
		
		return self._rest_request("/get-user-points/?user={0}".format(self.__username))
			
	def get_user_activities(self):
		if self.__logged_in == False:
			return False
		
		return self._rest_request("/get_user_activities/{0}".format(self.__user_id))
		