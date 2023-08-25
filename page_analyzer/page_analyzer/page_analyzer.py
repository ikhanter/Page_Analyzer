from dotenv import load_dotenv
from flask import (
    Flask,
)


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, Hexlet!', 200
