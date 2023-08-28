from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv
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
import psycopg2
import requests
from urllib.parse import urlparse
import validators


load_dotenv()
DB_FILE = 'database.sql'
DB_NAMES = ('pa_dev', 'pa_deploy')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    url = request.args.get('suggested_url', '')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages, suggested_url=url), 200  # noqa: E501


@app.route('/urls')
def urls():
    with conn.cursor() as cursor:
        cursor.execute('''SELECT id, name
                       FROM urls
                       ORDER BY urls.created_at DESC;''')
        temp = cursor.fetchall()
        result = []
        for el in temp:
            cursor.execute('''SELECT DATE(created_at), status_code
                           FROM url_checks
                           WHERE url_id=%(temp_id)s
                           ORDER BY created_at DESC LIMIT 1;''', {'temp_id': el[0]})   # noqa: E501
            temp_check = cursor.fetchone()
            if not temp_check:
                temp_check = tuple()
            element = el + temp_check
            result.append(element)
    return render_template('urls.html', url_list=result), 200


@app.route('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    with conn.cursor() as cursor:
        cursor.execute('SELECT name, DATE(created_at) FROM urls WHERE id=%s LIMIT 1;', (id,))  # noqa: E501
        url_temp = cursor.fetchone()
        if url_temp:
            url = {'name': url_temp[0], 'created_at': url_temp[1]}
            cursor.execute('''SELECT id, status_code, h1, title, description, DATE(created_at)
                           FROM url_checks
                           WHERE url_id=%s
                           ORDER BY created_at DESC;''', (id,))  # noqa: E501
            checks = cursor.fetchall()
        dict_keys = ('id', 'status_code', 'h1', 'title', 'description', 'created_at')
        all_checks = []
        for check in checks:
            all_checks.append(dict(zip(dict_keys, check)))
    return render_template('show_url.html', messages=messages, id=id, url=url, checks=all_checks), 200  # noqa: E501


@app.post('/urls')
def post_url():
    url = request.form['url']
    url_parsed = urlparse(url)
    if validators.url(url):
        with conn.cursor() as cursor:
            cursor.execute('''SELECT id
                           FROM urls
                           WHERE name=%(hostname)s
                           LIMIT 1;''', {'hostname': str(url_parsed.hostname)})
            result = cursor.fetchone()
            if result:
                messages = flash('Страница уже существует', 'info')
                return redirect(url_for('show_url', messages=messages, id=result[0]))  # noqa: E501
            cursor.execute('''INSERT INTO urls (name, created_at, scheme)
                           VALUES (%s, %s, %s);''', (url_parsed.hostname, datetime.datetime.now(), url_parsed.scheme))  # noqa: E501
            conn.commit()
            cursor.execute('''SELECT id
                           FROM urls
                           ORDER BY created_at DESC
                           LIMIT 1;''', (url_parsed.hostname))  # noqa: E501
            new_result = cursor.fetchone()[0]
        messages = flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', messages=messages, id=new_result), code=302)  # noqa: E501
    messages = flash('Некорректный URL', 'danger')
    return redirect(url_for('index', messages=messages, suggested_url=url))


@app.post('/urls/<int:id>/checks')
def post_check(id):
    with conn.cursor() as cursor:
        cursor.execute('''SELECT * FROM urls WHERE id=%(id)s LIMIT 1;''', {'id': id})  # noqa: E501
        result = cursor.fetchone()
        url = f'{result[3]}://{result[1]}'
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
        cursor.execute('''INSERT INTO url_checks
                       (url_id,
                       status_code,
                       h1,
                       title,
                       description,
                       created_at)
                       VALUES
                       (%(url_id)s,
                       %(status_code)s,
                       %(h1)s,
                       %(title)s,
                       %(description)s,
                       %(created_at)s);''',
                       {
                           'url_id': id,
                           'status_code': status_code,
                           'h1': h1,
                           'title': title,
                           'description': description,
                           'created_at': created_at,
                       })  # noqa: E501
        conn.commit()
    messages = flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id, messages=messages))
