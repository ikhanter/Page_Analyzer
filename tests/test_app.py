import pytest
from page_analyzer.page_analyzer import create_app


@pytest.fixture()
def app():
    new_app = create_app()
    yield new_app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_main_page(client):
    response = client.get('/')
    assert "Бесплатно проверяйте сайты на SEO-пригодность" in response.text


def test_urls_page(client):
    response = client.get('/urls')
    assert """<thead>
                            <tr>
                                <th>ID</th>
                                <th>Имя</th>
                                <th>Последняя проверка</th>
                                <th>Код ответа</th>
                            </tr>
                        </thead>""" in response.text


def test_add_url(client):
    response = client.post('/urls', data={
        'url': 'https://ru.hexlet.io'
    })
    assert response.status_code == 302
    assert 'Страница успешно добавлена' in response.text
    response = client.post('/urls', data={
        'url': 'https://ru.hexlet.io'
    })
    assert 'Страница уже существует' in response.text
    response = client.post('/urls', data={
        'url': 'asdf@dsj.dfkj'
    })
    assert 'Некорректный URL' in response.text

