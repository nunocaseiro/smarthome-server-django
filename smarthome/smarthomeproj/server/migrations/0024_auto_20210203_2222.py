# Generated by Django 3.1.3 on 2021-02-03 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0023_auto_20210203_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='key',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='housekey',
            name='key',
            field=models.CharField(blank=True, default='1559437149', editable=False, max_length=10, unique=True),
        ),
    ]