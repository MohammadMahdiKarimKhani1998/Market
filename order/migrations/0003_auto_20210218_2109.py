# Generated by Django 3.1.5 on 2021-02-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210121_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketitems',
            name='count',
            field=models.IntegerField(default=1, verbose_name='Count'),
        ),
        migrations.AddField(
            model_name='basketitems',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Price'),
        ),
    ]