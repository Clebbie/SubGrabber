from flask import Flask
from flask import request
from flask import render_template
from appdirs import *
import os
import subprocess
import requests
import json
import clipboard
import random

#Sets up a couple global items
#Flask => Local Webserver
#ClientID for the bot
#The subprocess that listens to the keyboard
app = Flask(__name__)
clientID = 'a0eq55k1fyehqztfwcr0bx6y9b8j5z'
keyboadListener = subprocess.Popen(["python","keystrokeListener.py"], stdout=None, stdin=subprocess.PIPE, stderr=None, shell = False)

#Data Directory for user.sg is /home/.local/share/SubGrabber
appDirectory = AppDirs('SubGrabber', 'Yarnball')

@app.route("/auth_success", methods = ['GET'])
def route_authSuccess():
	return render_template('auth_success.html')

@app.route("/", methods = ['GET'])
def index():
	accessToken = ''
	userID = ''
	isValid = False
	isFirstTime = not doesDataExist()
	#Verify if user information already exists on hand
	if(not isFirstTime):
		file = open(appDirectory.user_data_dir + '/user.sg', 'r')
		fileData = file.readlines()
		rawData = ''
		for line in fileData:
			rawData += line
		userInfo = json.loads(rawData)
		userID = userInfo['data'][0]['id']
		accessToken = userInfo['data'][0]['access_token']
		isValid = validateKey(accessToken)
	print('***************')
	print('accessToken = ' + accessToken + '\nuserID = ' + userID + '\nisFirstTime= ' + str(isFirstTime))
	return render_template('index.html', access_token=accessToken, user_id=userID, is_valid=isValid, first_time=isFirstTime)

@app.route("/auth", methods = ['POST'])
def route_auth():
	#TODO: create the user.sg
	data = request.get_json()
	print(data['access_token'])
	if(validateKey(data['access_token'])):
		createUserFile(data['access_token'])
		return 'Success!\n',200
	else:
		return 'Invalid or Expired key!\n', 401
	#run GET request to validate key
	#return true/ false
	return 'Success!\n',200
	#return 'Invalid!\n',401

def validateKey(key):
	twitchURL =  'https://id.twitch.tv/oauth2/validate'
	validationHeaderKey = 'Authorization'
	validationHeaderValue = 'OAuth ' + key
	response = requests.get(twitchURL,headers={validationHeaderKey : validationHeaderValue})

	data = json.loads(response.content.decode('utf-8'))

	print(data)
	#This is temp- it was ment to test functionality
	getUsersFollowers()

	if ('expires_in' in data and int(data['expires_in']) >= 60):
		print('***********\n')
		print(key + ' is valid')
		return True
	print('***********\n')
	print(key + ' is NOT valid')
	return False

def doesDataExist():
	#Look in user directory
	if(os.path.exists(appDirectory.user_data_dir)):
		print("NOT the first time")
		return True
	else:
		print('First time setup')
		return False
#Returns a JSON of the user from user.sg
def getUser():
	file = open(appDirectory.user_data_dir + '/user.sg','r')
	fileData = file.readlines()
	rawData = ''
	for line in fileData:
		rawData += line
	userInfo = json.loads(rawData)
	file.close()
	return userInfo

def createUserFile(access_token):
	if not doesDataExist():
		os.makedirs(appDirectory.user_data_dir)
	header = 'Authorization'
	url = 'https://api.twitch.tv/helix/users'
	response= requests.get(url,headers={header : 'Bearer ' + access_token})
	fileName = appDirectory.user_data_dir + '/user.sg'
	file = open(fileName, 'w+')
	data = json.loads(response.content)
	#data['data'][0]['access_token'] = access_token
	file.write(response.content)
	file.close()
	insertAccessToken(access_token)

def insertAccessToken(access_token):
	userInfor = ''
	file = open(appDirectory.user_data_dir + '/user.sg', 'r')
	fileData = file.readlines()
	rawData = ''
	for line in fileData:
		rawData += line
	userInfo = json.loads(rawData)
	userInfo['data'][0]['access_token'] = access_token
	fileName = appDirectory.user_data_dir + '/user.sg'
	file = open(fileName, 'w+')
	file.write(json.dumps(userInfo,ensure_ascii=True))
	file.close()

def getUsersFollowers():
	#Get User, format url, then execut GET request. This needs to be changed to subscribers not followers
	user = getUser()
	ClientKey = 'Client-ID'
	url = 'https://api.twitch.tv/kraken/channels/' +  user['data'][0]['id'] + '/follows'
	response = requests.get(url,headers={'Accept' : 'application/vnd.twitchtv.v5+json',ClientKey : clientID})
	followers = json.loads(response.content)
	total = int(followers['_total'])
	#Generate random number < the total number of followers returned. Then copy random follower to clipboard
	random.seed()
	randomName = followers['follows'][random.randint(0,total)]['user']['name']
	clipboard.copy(randomName)

if __name__ == "__main__":
    app.run()
