# Generated by Django 2.1.1 on 2018-10-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181018_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='where_to_status',
            field=models.CharField(choices=[('post_list', 'Post List'), ('post_list2', 'Post List2'), ('draft', 'Draft')], default='draft', max_length=15),
        ),
    ]
