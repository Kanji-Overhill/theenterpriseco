from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return 'Under Maintenance! Next relauch planing Jan 20, 2018, Thanks for your support!'
