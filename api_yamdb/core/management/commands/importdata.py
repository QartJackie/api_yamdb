import sqlite3

import pandas
from django.conf import settings
from django.core.management.base import BaseCommand


CSV_DATA_PATH = f'{settings.BASE_DIR}/static/data/'
DATA_TABLES = (
            ('titles.csv', 'reviews_title'),
            ('users.csv', 'users_customuser'),
            ('review.csv', 'reviews_review'),
            ('category.csv', 'reviews_category'),
            ('comments.csv', 'reviews_comment'),
            ('genre_title.csv', 'reviews_title_genre'),
            ('genre.csv', 'reviews_genre'),
        )
DATABASE_NAME = 'db.sqlite3'


class Command(BaseCommand):

    def base_connection(self):
        """Подключение к базе."""
        try:
            return sqlite3.connect(DATABASE_NAME)
        except Exception as connect_error:
            return f'Ошибка подключения к базе {DATABASE_NAME}.\
                     Код ошибки: {connect_error}'
        finally:
            print(f'Выполнено подключение к базе данных {DATABASE_NAME}.')

    def get_csv_data(self, filename, tablename, connection):
        """Извлечение данных из csv."""
        try:
            path = f'{settings.BASE_DIR}/static/data/{filename}'
            csv_data = pandas.read_csv(path, sep=',', header=0)
            csv_data.rename(
                columns={
                    'category': 'category_id',
                    'author': 'author_id'
                },
                inplace=True
            )
            csv_data.columns
            csv_data.to_sql(
                tablename, connection, if_exists='append', index=False
            )
        except Exception as extract_error:
            return f'Ошибка извлечения данных {extract_error}'
        finally:
            print(f'Файл {filename} успешно импортирован.')

    def handle(self, *args, **options):
        """Импорт данных."""
        try:
            connection = self.base_connection()
            for filename, tablename in DATA_TABLES:
                self.get_csv_data(filename, tablename, connection)
        except Exception as error:
            print(f'Импорт прерван: {error}')
        finally:
            print('Импорт завершен.')
