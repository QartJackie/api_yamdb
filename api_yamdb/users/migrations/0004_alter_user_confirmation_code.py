# Generated by Django 3.2 on 2023-03-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='I2XQ906FK5GG', max_length=50, null=True, verbose_name='Код подтверждения'),
        ),
    ]