from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/submit')
def submit_page():
	return render_template("submit.html")

if __name__ == "__main__":
	app.run()