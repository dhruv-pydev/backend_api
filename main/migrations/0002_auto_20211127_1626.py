# Generated by Django 3.2.9 on 2021-11-27 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50)),
            ],
        ),
        migrations.AlterModelOptions(
            name='baseuser',
            options={'verbose_name': 'Base Users'},
        ),
    ]
