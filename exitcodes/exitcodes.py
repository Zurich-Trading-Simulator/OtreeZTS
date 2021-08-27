from otree.models import Session
from otree.api import safe_json
# from Crypto.Cipher import AES
# from Crypto.Hash import SHA
import hashlib
from datetime import datetime
import json
import os

folder = '__access-exitcodes/'
date = datetime.now().strftime("%Y-%m-%d")

def hash_and_save_csv(participants, session_code, url):
	"""
	participants is the participants list
	session_code is the current session code
	url is the participant start url
	for example:
		http://192.168.99.100:3000/InitializeParticipant/
		or
		http://example.com/InitializeParticipant/
	"""
	codes = [participant.code for participant in participants]
	hashed = hash_participant_codes(codes)
	try:
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(folder+date +"_"+ session_code + ".csv", 'x') as out:
			print(out.name, 'does not yet exist')

			out.write('AccessCode,ExitCode'+'\n')     
			for code_exit_code in hashed:
				out.write(code_exit_code['AccessCode']+','+code_exit_code['ExitCode']+'\n')
	except:
		print(folder+date +"_"+ session_code + ".csv", 'does already exist')


def hash_and_save_json(participants, session_code, url=""):
	"""
	participants is the participants list
	session_code is the current session code
	see above
	"""
	codes = [participant.code for participant in participants]
	# Choose Hashing or Encrypting here
	hashed = hash_participant_codes(codes)
	try:
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(folder+date +"_"+ session_code + ".json", 'x') as out:
			print(out.name, 'does not yet exist')

			json.dump(hashed, out, indent=4)
			safe_json(hashed)
	except:
		print(folder+date +"_"+ session_code + ".json", 'does already exist')

	return hashed

def hash_participant_codes(codes):
	"""
	Hash the participants codes
	"""
	return [{'AccessCode': code,
			 'ExitCode': sha_hash(code)} for code in codes]

def sha_hash(string):
	# b: Specify the length of the codes here
	# return SHA.new(string.encode()).hexdigest()[:8]
	return hashlib.sha256(string.encode()).hexdigest()[:8]