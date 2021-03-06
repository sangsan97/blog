# Generated by Django 2.1.2 on 2018-11-04 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_publication_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('where_to_status', models.CharField(choices=[('postdoc', 'Post Doctorate'), ('phd', 'PhD.'), ('master', 'Master Degree'), ('visiting', 'Visiting Student')], default='master', max_length=20)),
            ],
        ),
    ]
