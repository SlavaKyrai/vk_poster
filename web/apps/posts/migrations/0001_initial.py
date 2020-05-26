# Generated by Django 3.0.5 on 2020-05-19 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('vk_name', models.CharField(max_length=100, unique=True)),
                ('vk_community_id', models.IntegerField(primary_key=True, serialize=False)),
                ('subbredit_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VKToken',
            fields=[
                ('token', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('reddit_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True)),
                ('self_text', models.TextField(blank=True)),
                ('is_self', models.BooleanField()),
                ('score', models.IntegerField(blank=True, default=0)),
                ('url', models.URLField()),
                ('is_posted', models.BooleanField(default=False)),
                ('vk_community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Community')),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.VKToken'),
        ),
    ]
