from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    url_for,
)


load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/urls')
def urls():
    return 'Placeholder'
