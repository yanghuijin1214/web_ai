# Generated by Django 3.2.7 on 2021-11-30 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='predict',
            field=models.CharField(default='', max_length=50, null=True, verbose_name='예측결과'),
        ),
    ]
