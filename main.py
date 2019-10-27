from flask import Flask
from flask import request
from flask import render_template
import requests
import json
app = Flask(__name__)

clientID = 'a0eq55k1fyehqztfwcr0bx6y9b8j5z'


@app.route("/auth_success", methods = ['GET'])
def route_authSuccess():
	return render_template('auth_success.html')

@app.route("/", methods = ['GET'])
def index():
	accessToken = ''
	userID = ''
	isValid = False
	isFirstTime = True
	return render_template('index.html', access_token=accessToken, user_id=userID, is_valid=isValid, first_time=isFirstTime)

@app.route("/auth", methods = ['POST'])
def route_auth():
	data = request.get_json()
	print(data['access_token'])
	if(validateKey(data['access_token'])):
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
	if(int(data['expires_in']) <= 60):
		return False
	return True

if __name__ == "__main__":
    app.run()
