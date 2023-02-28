from django.core.management.base import BaseCommand
# import csv
# from api_yamdb.settings import BASE_DIR

from reviews.models import Category, Genre, Title


TABLES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv'
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print('starting import')
        # for model, csv_filename in TABLES.items():
        #     with open(
        #         f'{BASE_DIR}/static/data/{csv_filename}',
        #         'r',
        #         encoding='utf-8'
        #     ) as csv_file:
        #         reader = csv.DictReader(csv_file)
        #         model.objects.bulk_create(
        #             model(**data) for data in reader
        #         )
