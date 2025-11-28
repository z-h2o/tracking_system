import os
import django
import pymysql
from django.conf import settings as django_settings
from .config import settings

# 使用 PyMySQL 作为 MySQLdb 的替代
pymysql.install_as_MySQLdb()

def setup_django():
    """初始化Django ORM"""
    if not django_settings.configured:
        django_settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': settings.DB_NAME,
                    'USER': settings.DB_USER,
                    'PASSWORD': settings.DB_PASSWORD,
                    'HOST': settings.DB_HOST,
                    'PORT': settings.DB_PORT,
                    'OPTIONS': {
                        'charset': 'utf8mb4',
                        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                    },
                    'CONN_MAX_AGE': 600,
                }
            },
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
            ],
            USE_TZ=True,
            TIME_ZONE='Asia/Shanghai',
        )
        django.setup()