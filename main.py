from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
	print('This is headers:\n' + str(request.headers))
	print('This is data:\n' + str(request.data))
	print('This is url:\n' + str(request.url))
	print(request.args.to_dict())
	return 'Success',200

if __name__ == "__main__":
    app.run()
