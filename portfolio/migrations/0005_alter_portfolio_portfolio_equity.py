# Generated by Django 4.2.1 on 2023-08-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_portfolio_portfolio_equity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='portfolio_equity',
            field=models.JSONField(default=dict),
        ),
    ]
