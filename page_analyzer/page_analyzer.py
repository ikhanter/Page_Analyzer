from bs4 import BeautifulSoup
from page_analyzer.database import DatabaseConnection
from page_analyzer.url_repository import UrlRepository
import datetime
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
import requests
from urllib.parse import urlparse
import validators


DB_NAMES = ('pa_dev', 'pa_deploy')
db_connector = DatabaseConnection()
url_repo = UrlRepository(db_connector)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    url = request.args.get('suggested_url', '')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages, suggested_url=url), 200  # noqa: E501


@app.route('/urls')
def urls():
    all_urls = url_repo.get_all_urls()
    result = []
    for url in all_urls:
        last_check = url_repo.get_last_check_for_url_by_id(url['id'])
        result.append({**url, **last_check})
    return render_template('urls.html', url_list=result), 200


@app.route('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = url_repo.get_url_by_id(id)
    if url:
        checks = url_repo.get_checks_by_url_id(id)
    return render_template('show_url.html', messages=messages, id=id, url=url, checks=checks), 200  # noqa: E501


@app.post('/urls')
def post_url():
    url = request.form['url']
    url_parsed = urlparse(url)
    if validators.url(url):
        result = url_repo.get_url_by_hostname(url_parsed.hostname)
        if result:
            messages = flash('Страница уже существует', 'info')
            return redirect(url_for('show_url', messages=messages, id=result['id']))  # noqa: E501
        url_repo.add_url(url_parsed.hostname, datetime.datetime.now(), url_parsed.scheme)  # noqa: E501
        new_result = url_repo.get_url_by_hostname(url_parsed.hostname)
        messages = flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', messages=messages, id=new_result['id']), code=302)  # noqa: E501
    messages = flash('Некорректный URL', 'danger')
    return redirect(url_for('index', messages=messages, suggested_url=url))


@app.post('/urls/<int:id>/checks')
def post_check(id):
    try:
        result = url_repo.get_url_by_id(id)
        url = f"{result['scheme']}://{result['name']}"
        r = requests.get(url)
        html = BeautifulSoup(r.text)
        status_code = r.status_code
        title = html.title
        title = title.text if title else ''
        h1 = html.h1
        h1 = h1.text if h1 else ''
        description = html.find('meta', property="og:description")
        description = description['content'] if description else ''
        created_at = datetime.datetime.now()
        url_repo.add_check(url_id=id,
                           status_code=status_code,
                           h1=h1,
                           title=title,
                           description=description,
                           created_at=created_at)
        messages = flash('Страница успешно проверена', 'success')
    except Exception: 
        messages = flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('show_url', id=id, messages=messages))
