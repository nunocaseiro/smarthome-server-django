# Generated by Django 3.1.3 on 2021-02-09 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0030_auto_20210207_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekey',
            name='key',
            field=models.CharField(blank=True, default='6125745093', editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='roomtype',
            field=models.CharField(choices=[('bedroom', 'BEDROOM'), ('garage', 'GARAGE'), ('kitchen', 'KITCHEN'), ('living', 'LIVING ROOM'), ('bathroom', 'BATHROOM'), ('other', 'OTHER')], default='bedroom', max_length=20),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='licenseplate',
            field=models.CharField(max_length=6),
        ),
    ]
