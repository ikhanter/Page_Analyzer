from page_analyzer.url_services import UrlServices
from page_analyzer.database import DatabaseConnection
from page_analyzer.url_repository import UrlRepository
from flask import (
    abort,
    flash,
    Flask,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
import os


def create_app():
    new_app = Flask(__name__)
    return new_app


db_connector = DatabaseConnection()
url_repo = UrlRepository(db_connector)
app = create_app()
app.secret_key = os.getenv('SECRET_KEY')
functionality = UrlServices(url_repo)


@app.route('/')
def index():
    url = request.args.get('suggested_url', '')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages, suggested_url=url), 200  # noqa: E501


@app.route('/urls/')
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
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
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
            new_messages = get_flashed_messages(with_categories=True)
            return render_template('index.html', messages=new_messages, suggested_url=url), 422  # noqa: E501


@app.post('/urls/<int:id>/checks')
def post_check(id):
    feedback = functionality.make_check(id)
    messages = flash(*feedback)
    return redirect(url_for('show_url', id=id, messages=messages))
