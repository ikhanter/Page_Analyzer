import copy
import datetime
from page_analyzer.url_services import UrlServices
import pook
import pytest


class FakeRepo:
    all_urls = [
        {
            'id': 1,
            'name': 'ru.hexlet.io',
            'created_at': '2000-11-11',
            'scheme': 'https'
        },
        {
            'id': 2,
            'name': 'www.google.com',
            'created_at': '1998-10-9',
            'scheme': 'http'
        },
        {
            'id': 3,
            'name': 'vk.com',
            'created_at': '2020-10-9',
            'scheme': 'https'
        },
    ]
    all_checks = [
        {
            'url_id': 1,
            'checks': []
        },
        {
            'url_id': 2,
            'checks': [
                {
                    'id': 3,
                    'status_code': 200,
                    'h1': 'Test id 3',
                    'title': '2nd check',
                    'description': 'Test check',
                    'created_at': '1998-10-10'
                },
                {
                    'id': 1,
                    'status_code': 200,
                    'h1': 'Test id 1',
                    'title': '1st check',
                    'description': 'Test check',
                    'created_at': '1998-10-9'
                },
            ]
        },
        {
            'url_id': 3,
            'checks': [
                {
                    'id': 2,
                    'status_code': 404,
                    'h1': 'Test',
                    'title': 'Test for 404',
                    'description': 'Page not found',
                    'created_at': '2020-10-10'
                },
            ]
        }
    ]

    def get_all_urls(self):
        new_list = copy.deepcopy(self.all_urls)
        for el in new_list:
            del el['scheme']
        return sorted(new_list, key=lambda x: datetime.datetime.strptime(x['created_at'], '%Y-%m-%d'), reverse=True)  # noqa: E501

    def get_last_check_for_url_by_id(self, url_id):
        result = self.get_checks_by_url_id(url_id)
        if result:
            result = result[0]
            return {
                'last_check_created_at': result['created_at'],
                'last_check_status_code': result['status_code'],
            }
        return {
            'last_check_created_at': '',
            'last_check_status_code': '',
        }

    def get_url_by_id(self, url_id):
        for url in self.all_urls:
            if url['id'] == url_id:
                new_dict = copy.deepcopy(url)
        del new_dict['id']
        return new_dict

    def get_checks_by_url_id(self, url_id):
        for url in self.all_checks:
            if url['url_id'] == url_id:
                new_list = copy.deepcopy(url['checks'])
                if new_list != []:
                    return sorted(new_list, key=lambda x: datetime.datetime.strptime(x['created_at'], '%Y-%m-%d'), reverse=True)  # noqa: E501
                return new_list

    def get_url_by_hostname(self, hostname):
        for url in self.all_urls:
            if url['name'] == hostname:
                new_dict = copy.deepcopy(url)
                del new_dict['scheme']
                return new_dict
        return False

    def add_url(self, hostname, date, scheme):
        max_id = sorted(self.all_urls, key=lambda x: -x['id'])[0]['id']
        self.all_urls.append({
            'id': max_id + 1,
            'name': hostname,
            'created_at': date,
            'scheme': scheme
        })

    def add_check(self, url_id='', status_code='', h1='', title='', description='', created_at=''):  # noqa: E501
        for url in self.all_checks:
            if url['url_id'] == url_id:
                if url['checks']:
                    max_check_id = sorted(url['checks'], key=lambda x: x['id'])[0]['id']  # noqa: E501
                else:
                    max_check_id = 0
                url['checks'].append({
                    'id': max_check_id + 1,
                    'status_code': status_code,
                    'h1': h1,
                    'title': title,
                    'description': description,
                    'created_at': created_at.strftime('%Y-%m-%d')
                })


@pytest.fixture()
def functionality():
    fake_repo = FakeRepo()
    functionality = UrlServices(fake_repo)
    return functionality


def test_form_urls_with_last_check(functionality):
    correct = [
        {
            'id': 3,
            'name': 'vk.com',
            'created_at': '2020-10-9',
            'last_check_created_at': '2020-10-10',
            'last_check_status_code': 404,
        },
        {
            'id': 1,
            'name': 'ru.hexlet.io',
            'created_at': '2000-11-11',
            'last_check_created_at': '',
            'last_check_status_code': '',
        },
        {
            'id': 2,
            'name': 'www.google.com',
            'created_at': '1998-10-9',
            'last_check_created_at': '1998-10-10',
            'last_check_status_code': 200,
        },
    ]
    result = functionality.form_urls_with_last_check()
    assert result == correct


def test_process_url_in_db(functionality):
    already_in = functionality.process_url_in_db('https://ru.hexlet.io')
    new_one = functionality.process_url_in_db('https://ok.ru')
    incorrect = functionality.process_url_in_db('httpssss://abc@abc.net')
    assert already_in == {
        'status': 'info',
        'message': 'Страница уже существует',
        'content': 1
    }
    assert new_one == {
        'status': 'success',
        'message': 'Страница успешно добавлена',
        'content': 4
    }
    assert incorrect == {
        'status': 'danger',
        'message': 'Некорректный URL',
        'content': 'httpssss://abc@abc.net'
    }


@pook.on
def test_make_check(functionality):
    pook.get('https://ru.hexlet.io', reply=200, response_type='text/html', response_body='<html><head><title>Test title</title><meta name="description" content="Test description for Page Analyzer"></head><body><h1>Test h1</h1></body></html>')  # noqa: E501
    pook.get('http://www.google.com', reply=500, response_type='text/html', response_body='<html><head><title>Test for bad</title></лдодлhead></html>')  # noqa: E501
    result_good = functionality.make_check(1)
    result_bad = functionality.make_check(2)
    assert result_good == ('Страница успешно проверена', 'success')
    assert result_bad == ('Произошла ошибка при проверке', 'danger')
