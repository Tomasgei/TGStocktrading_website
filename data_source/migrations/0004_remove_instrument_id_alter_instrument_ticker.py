# Generated by Django 4.2.1 on 2023-05-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_source', '0003_alter_historicaldata_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='id',
        ),
        migrations.AlterField(
            model_name='instrument',
            name='ticker',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='ticker'),
        ),
    ]
