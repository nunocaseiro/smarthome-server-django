# Generated by Django 3.1.3 on 2021-02-03 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Key', models.CharField(blank=True, default='9770989911', editable=False, max_length=10, unique=True)),
            ],
        ),
    ]
