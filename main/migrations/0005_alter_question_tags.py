# Generated by Django 3.2.9 on 2021-11-27 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211127_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(db_index=True, related_name='question_tags', to='main.Tag'),
        ),
    ]
