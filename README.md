### GitHub Actions
[![Actions Status](https://github.com/ikhanter/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/ikhanter/python-project-83/actions)
[![Actions Status](https://github.com/ikhanter/python-project-83/workflows/CI/badge.svg)](https://github.com/ikhanter/python-project-83/actions)

### CodeClimate
[![Maintainability](https://api.codeclimate.com/v1/badges/421eb636f069de274c35/maintainability)](https://codeclimate.com/github/ikhanter/python-project-83/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/421eb636f069de274c35/test_coverage)](https://codeclimate.com/github/ikhanter/python-project-83/test_coverage)

## Link: [click](https://page-analyzer-bcx7.onrender.com)
The web service may be deactivated due to the expiration of the free operating time of the database and the service itself. Please write to me to activate the service and rebuild the database.

# About

Web service for checking website metadata with database.

# System requirements

#### PL, Virtual Environment, DBMS

- Python 3.10 or above
- Poetry 1.5.1 or above
- PostgreSQL 14.9

#### Modules

- Flask 2.3.3 or above
- gunicorn 20.1.0 or above
- python-dotenv 1.0.0 or above
- validators 0.21.2 or above
- psycopg2-binary 2.9.7 or above
- requests 2.31.0 or above
- BeautifulSoup4 4.12.2 or above
- pook 1.1.1 or above

#### Linter and tests

- pytest 7.4.2 or above
- pytest-cov 4.1.0 or above
- ruff 0.0.290 or above

# Installing

The command below will install all dependencies and database template for correct work of the web-service locally or on a deploy.

```make build```

After installing file ".env" should be created in the root directory of the project. This file must contain environment variables:
- SECRET_KEY
- DATABASE_URL
- PORT

On a deployment these variables should be defined on your deploy service. 

# Dev mode with debug

```make dev```

# Launch web-service

```make start```
