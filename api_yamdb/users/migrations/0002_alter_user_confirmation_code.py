# Generated by Django 3.2 on 2023-03-03 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='12OTV7AX6HGC', max_length=50, null=True, verbose_name='Код подтверждения'),
        ),
    ]
