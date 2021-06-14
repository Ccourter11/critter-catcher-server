# Generated by Django 3.2.4 on 2021-06-14 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=50)),
                ('date', models.DateTimeField(max_length=50)),
                ('image_url', models.CharField(max_length=50)),
                ('is_complete', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crittercatcherapi.category')),
            ],
        ),
        migrations.CreateModel(
            name='Requestor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=250)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crittercatcherapi.request')),
                ('requestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crittercatcherapi.requestor')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='requestor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crittercatcherapi.requestor'),
        ),
    ]
