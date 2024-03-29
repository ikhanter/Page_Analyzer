class UrlRepository:
    connector = None

    def __init__(self, connector):
        self.connector = connector

    def get_all_urls(self):
        result = self.connector.execute('SELECT id, name, created_at FROM urls ORDER BY created_at DESC;')  # noqa: E501
        total = []
        keys = ('id', 'name', 'created_at')
        for el in result:
            total.append(dict(zip(keys, el)))
        return total

    def get_last_check_for_url_by_id(self, id):
        result = self.connector.execute('''SELECT DATE(created_at), status_code
                        FROM url_checks
                        WHERE url_id=%(id)s
                        ORDER BY created_at DESC;''', {'id': id}, get_back='one')  # noqa: E501
        keys = ('last_check_created_at', 'last_check_status_code')
        if result:
            total = dict(zip(keys, result))
            return total
        return dict(zip(keys, ('', '')))

    def get_url_by_id(self, id):
        result = self.connector.execute('''SELECT name, DATE(created_at), scheme
                                                 FROM urls
                                                 WHERE id=%s;''', (id,), get_back='one')  # noqa: E501
        if result:
            keys = ('name', 'created_at', 'scheme')
            return dict(zip(keys, result))
        return None

    def get_checks_by_url_id(self, id):
        checks_temp = self.connector.execute('''SELECT id, status_code, h1, title, description, DATE(created_at)
                        FROM url_checks
                        WHERE url_id=%s
                        ORDER BY created_at DESC;''', (id,))  # noqa: E501
        keys = ('id', 'status_code', 'h1', 'title', 'description', 'created_at')
        checks = []
        for check in checks_temp:
            checks.append(dict(zip(keys, check)))
        return checks

    def get_url_by_hostname(self, hostname):
        result = self.connector.execute('''SELECT id, name, created_at
                           FROM urls
                           WHERE name=%(hostname)s;''', {'hostname': str(hostname)}, get_back='one')  # noqa: E501
        if result:
            keys = ('id', 'name', 'created_at')
            return dict(zip(keys, result))
        return None

    def add_url(self, hostname, date, scheme):
        self.connector.execute('''INSERT INTO urls (name, created_at, scheme)
                               VALUES (%s, %s, %s);''', (hostname, date, scheme), get_back='none')  # noqa: E501

    def add_check(self, url_id='', status_code='', h1='', title='', description='', created_at=''):  # noqa: E501
        self.connector.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                               VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s, %(created_at)s);''',  # noqa: E501
                               {'url_id': url_id,
                                'status_code': status_code,
                                'h1': h1,
                                'title': title,
                                'description': description,
                                'created_at': created_at}, get_back='none')
