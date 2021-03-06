# Generated by Django 3.1.3 on 2021-02-03 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0018_auto_20210203_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekey',
            name='key',
            field=models.CharField(blank=True, default='7351451907', editable=False, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='home',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='server.home'),
        ),
    ]
