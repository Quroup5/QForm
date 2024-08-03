# QForm

A toy Python project for a dynamic form generation system

### Project Setup

- SECRET_KEY *(required)*: Secret key for the Django project. Must be kept confidential.
- DEBUG: (boolean) Default is True. Toggle debug mode.
- FERNET_KEY: *(required)*(str): The Key For Encrypt And Masking
  Datas. [For Info Visit](https://pypi.org/project/redis-management/)

### Database Configuration

- PostgreSQL
    - PG_NAME: (string) Name of the PostgreSQL database.
    - PG_USER: (string) PostgreSQL username.
    - PG_PASSWORD: (string) PostgreSQL password.
    - PG_HOST: (URL) PostgreSQL host URL.
    - PG_PORT: (int) PostgreSQL port number.

### Email Hosting

- DEPENDENT_EMAIL_ON_DEBUG: (boolean) Default is True. If True, email messages are managed on the console in debug
  mode. Set to False to receive email messages in debug mode.
- EMAIL_HOST: (string) Host for the email server.
- EMAIL_HOST_USER: (string) Username for the email server.
- EMAIL_HOST_PASSWORD: (string) Password for the email server.
- EMAIL_PORT: (int) Port for the email server.
- EMAIL_USE_SSL: (boolean) Enable SSL for email.
- EMAIL_USE_TLS: (boolean) Enable TLS for email.
- DEFAULT_FROM_EMAIL: (string) Default email address for sending emails.

### Redis Setup

- REDIS_HOST: (URL) Default is localhost. Redis host URL.
- REDIS_PORT: (int) Default is 6379. Redis port number.
- REDIS_DB: (int) Default is 0. Redis database number.
- FERNET_KEY: *(required)*(str): The Key For Encrypt Codes In
  Redis. [For Info Visit](https://pypi.org/project/redis-management/)

## How to Install and Host Mail Server with Docker

For installing and hosting a mail server with Docker, visit:
[Use Docker Mailserver to Build Self-hosted Mail Server](https://henrywithu.com/use-docker-mailserver-to-build-self-hosted-mail-server/)

## How To Run Docker :question:

To run Docker, execute:
```bash
docker-compose up -d
```


## How To Run Locally :question:

To run the project locally:

```python
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver or gunicorn src.config.wsgi:application --bind 0.0.0.0:8000
```

Or use Gunicorn:
```bash
gunicorn src.config.wsgi:application --bind 0.0.0.0:8000
```



## For Installing Redis

On Linux (Ubuntu):

```bash
sudo apt-get install redis-server
sudo service redis-server start
```

On Windows:

Turn on Windows Subsystem for Linux:
```bash
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```


Launch Microsoft Windows Store:

start ms-windows-store:


Install Redis server:
```bash
sudo apt-add-repository ppa:redislabs/redis
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis-server
```


