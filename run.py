from flask import Flask
from dotenv import load_dotenv

from config import config

#loads env variables from the .env file
load_dotenv()

#sets the flask app
app = Flask(__name__)
app.config.from_object(config["development"])

@app.route("/")
def index():
    return "Hello"

if __name__ == "__main__":
    app.run()