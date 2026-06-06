from flask import Flask

from main import main

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

@app.route("/run-daily")
def run_daily():

    main()

    return "Done"