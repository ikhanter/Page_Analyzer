from page_analyzer.business_logic import Logic
from page_analyzer.database import DatabaseConnection
from page_analyzer.url_repository import UrlRepository
from flask import (
    flash,
    Flask,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
import os


DB_NAMES = ('pa_dev', 'pa_deploy')
db_connector = DatabaseConnection()
url_repo = UrlRepository(db_connector)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
functionality = Logic(url_repo)


@app.route('/')
def index():
    url = request.args.get('suggested_url', '')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages, suggested_url=url), 200  # noqa: E501


@app.route('/urls')
def urls():
    result = functionality.form_urls_with_last_check()
    return render_template('urls.html', url_list=result), 200


@app.route('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = url_repo.get_url_by_id(id)
    if url:
        checks = url_repo.get_checks_by_url_id(id)
        return render_template('show_url.html', messages=messages, id=id, url=url, checks=checks), 200  # noqa: E501
    return render_template('404.html'), 404


@app.post('/urls')
def post_url():
    url = request.form['url']
    result = functionality.process_url_in_db(url)
    messages = flash(result['message'], result['status'])
    match result['status']:
        case 'success':
            return redirect(url_for('show_url', messages=messages, id=result['content']), code=302)  # noqa: E501
        case 'info':
            return redirect(url_for('show_url', messages=messages, id=result['content']))  # noqa: E501
        case 'danger':
            return redirect(url_for('index', messages=messages, suggested_url=result['content']), code=422)  # noqa: E501


@app.post('/urls/<int:id>/checks')
def post_check(id):
    feedback = functionality.make_check(id)
    messages = flash(*feedback)
    return redirect(url_for('show_url', id=id, messages=messages))
