from bs4 import BeautifulSoup
import datetime
import validators
from page_analyzer.url_repository import UrlRepository
import requests
from urllib.parse import urlparse


class Logic:
    url_repo_connector = None

    def __init__(self, url_repo: UrlRepository):
        self.url_repo_connector = url_repo

    def form_urls_with_last_check(self):
        url_list = self.url_repo_connector.get_all_urls()
        result = []
        for url in url_list:
            last_check = self.url_repo_connector.get_last_check_for_url_by_id(url['id'])  # noqa: E501
            result.append({**url, **last_check})
        return result

    def process_url_in_db(self, url):
        url_parsed = urlparse(url)
        feedback = {'status': None, 'message': None, 'content': None}
        if validators.url(url):
            result = self.url_repo_connector.get_url_by_hostname(url_parsed.hostname)  # noqa: E501
            if result:
                feedback['status'] = 'info'
                feedback['message'] = 'Страница уже существует'
                feedback['content'] = result['id']
            else:
                self.url_repo_connector.add_url(url_parsed.hostname, datetime.datetime.now(), url_parsed.scheme)  # noqa: E501
                new_result = self.url_repo_connector.get_url_by_hostname(url_parsed.hostname)  # noqa: E501
                feedback['status'] = 'success'
                feedback['message'] = 'Страница успешно добавлена'
                feedback['content'] = new_result['id']
        else:
            feedback['status'] = 'danger'
            feedback['message'] = 'Некорректный URL'
            feedback['content'] = str(url)
        return feedback

    def make_check(self, id):
        try:
            result = self.url_repo_connector.get_url_by_id(id)
            url = f"{result['scheme']}://{result['name']}"
            r = requests.get(url)
            r.raise_for_status()
            html = BeautifulSoup(r.text, features="html.parser")
            status_code = r.status_code
            title = html.title
            title = title.text if title else ''
            h1 = html.h1
            h1 = h1.text if h1 else ''
            description = html.find('meta', attrs={'name': "description"})
            description = description['content'] if description else ''
            created_at = datetime.datetime.now()
            self.url_repo_connector.add_check(url_id=id,
                                              status_code=status_code,
                                              h1=h1,
                                              title=title,
                                              description=description,
                                              created_at=created_at)
            messages = ('Страница успешно проверена', 'success')
        except Exception:
            messages = ('Произошла ошибка при проверке', 'danger')
        finally:
            return messages
