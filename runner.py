from sys import argv, exit

from fitocracy_extension_app import *
from parse_credential_file import *

if not (len(argv) == 2 and argv[1]):
	print("Usage: runner.py [credentialfile.txt]")
	exit(1)
	
print("Beginning log in")

parsefile = ParseCredentialFile(argv[1])

frs = FitocracyRestSession()

if frs.login(parsefile.get_username(), parsefile.get_password()):
	print("Successful log in.")
else:
	print("Error. Log in failed")
	exit(1)
	
print("==============================")

while True:
	print("[1] Full Activity Breakdown")
	print("[2] Print user info")
	print("[3] Print workout breakdown")
	print("[4] Max Breakdown of each exercise with date.")
	print("[0] Exit\n")

	try:
		a_input = int(raw_input("Enter command: "))

		if a_input == 1:
			print frs.get_user_activities() 
		elif a_input == 2:
			print("Your UID: {0}".format(frs.get_user_id()))
			print("Your username: {0}".format(frs.get_username()))
		elif a_input == 3:
			print("Your recent activity: {0}".format(frs.get_user_points()))
		elif a_input == 0:
			print("Exit program")
			exit(1)
		else:
			print("Not implemented yet")
	except ValueError:
		print("Not a valid number")
		
	print("\n\n\n")