from sys import argv, exit

from fitocracy_extension_app import *
from parse_credential_file import *

if not (len(argv) == 2 and argv[1]):
	print("Usage: runner.py [credentialfile.txt]")
	exit(1)
	
print("Beginning log in")

parsefile = ParseCredentialFile(argv[1])

fitologin = FitocracyLogin(parsefile.get_username(), parsefile.get_password())

if fitologin.checkLoggedIn() != True:
	print("Error. Log in failed")
	exit(1)
	
#Assume logged in correctly from here on.
print("Successful log in.")
fps = FitocracyParserSession(fitologin.getOpenerObject())

print("==============================")

while True:
	print("[1] Full Activity Breakdown")
	print("[2] Print user info")
	print("[3] Print workout breakdown")
	print("[4] Output activity breakdown.")
	print("[5] Max Breakdown of each exercise with date.")
	print("[0] Exit\n")

	try:
		a_input = int(raw_input("Enter command: "))
	except ValueError:
		print("Not a valid number")
	
	if a_input == 1:
		print fps.get_user_activities() 
	elif a_input == 2:
		print("Your UID: {0}".format(fps.get_user_id()))
		print("Your username: {0}".format(fps.get_username()))
	elif a_input == 3:
		print("Your recent activity: {0}".format(fps.get_user_points()))
	#elif a_input == 4:
#		fps.update_current_workout()
	elif a_input == 0:
		print("Exit program")
		exit(1)
	else:
		print("Not implemented yet")
	
		
	print("\n\n\n")