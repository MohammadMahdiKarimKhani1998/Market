# Generated by Django 3.1.5 on 2021-02-18 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210218_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitems',
            name='count',
            field=models.IntegerField(verbose_name='Count'),
        ),
        migrations.AlterField(
            model_name='basketitems',
            name='price',
            field=models.IntegerField(verbose_name='Price'),
        ),
    ]
