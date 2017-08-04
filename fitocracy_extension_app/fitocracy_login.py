#FitocracyLogin

import json
import re
import os

import cookielib
import urllib2
import urllib 

class FitocracyLogin(object):
	def __init__(self, user, password):
		self.__BASE_URL = "https://www.fitocracy.com"
		self.__cookie_jar = cookielib.CookieJar()
		self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cookie_jar))
		
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
						
		self.__logged_in = False if "<!-- end of login modal -->" in str(response.read()) else True
	
	def getOpenerObject(self):
		return self.__opener
	
	def checkLoggedIn(self):
		return self.__logged_in