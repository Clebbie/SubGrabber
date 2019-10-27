from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route("/auth_success", methods = ['GET'])
def hello():
	return render_template('auth_success.html')

@app.route("/auth", methods = ['POST'])
def getBody():
	data = request.get_json()
	print(data)
	return 'Success!\n',200
if __name__ == "__main__":
    app.run()
