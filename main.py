from datetime import datetime

from redis import Redis

from flask import Flask, session, render_template
from flask.ext.session import Session

from extensions import PollRedis

app = Flask(__name__, template_folder=".")


SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

cr = PollRedis(app)

@app.route("/")
def index():
    return render_template('poll.html')

@app.route("/result")
def result():
    return render_template('poll_result.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
