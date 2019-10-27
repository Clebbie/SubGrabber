from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route("/auth_success", methods = ['GET'])
def hello():
	return render_template('auth_success.html')

@app.route("/", methods = ['GET'])
def index():
	accessToken = 'Test'
	userID = "Dank"
	return render_template('index.html', access_token=accessToken, user_id=userID)

@app.route("/auth", methods = ['POST'])
def validateKey():
	data = request.get_json()
	print(data)
#run GET request to validate key
	#return true/ false
	return 'Success!\n',200



if __name__ == "__main__":
    app.run()
