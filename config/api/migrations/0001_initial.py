# Generated by Django 3.0.5 on 2022-03-13 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Listener',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='username')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
            ],
            options={
                'verbose_name': 'lister',
                'verbose_name_plural': 'lister',
            },
        ),
        migrations.CreateModel(
            name='Sync',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(max_length=254)),
                ('guests', models.ManyToManyField(to='api.Listener')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='channel name')),
                ('rules', models.TextField(null=True, verbose_name='rules')),
                ('playlist_id', models.CharField(max_length=254, verbose_name='playlist id')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Creator', to='api.Listener')),
                ('guests', models.ManyToManyField(to='api.Listener')),
                ('sync', models.ManyToManyField(to='api.Sync')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'room',
            },
        ),
        migrations.AddIndex(
            model_name='listener',
            index=models.Index(fields=['username'], name='lister_username_idx'),
        ),
    ]
