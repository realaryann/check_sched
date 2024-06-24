from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():		
	return render_template("index.html")

@app.route('/submit', methods=["POST","GET"])
def submit_page():
	return render_template("submit.html")

if __name__ == "__main__":
	app.run()