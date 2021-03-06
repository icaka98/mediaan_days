# Generated by Django 2.1.3 on 2018-11-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NumVar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.DecimalField(decimal_places=3, default=0.0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='OffDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(verbose_name='day off')),
                ('desc', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StrVar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=254)),
            ],
        ),
    ]
