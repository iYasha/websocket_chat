"""
Файл утилит для чата
"""
import os
if os.getenv('DATABASE') == 'postgresql':
    import psycopg2


def _postgres_connection():
    connection = psycopg2.connect(user=os.getenv('DATABASE_USER'),
                                  password=os.getenv('DATABASE_PASSWORD'),
                                  host=os.getenv('DATABASE_HOST'),
                                  port=os.getenv('DATABASE_PORT'),
                                  database=os.getenv('DATABASE_NAME'))
    return connection


def get_connection():
    if os.getenv('DATABASE') == 'postgresql':
        return _postgres_connection()
