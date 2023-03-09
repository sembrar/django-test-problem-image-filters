# Generated by Django 4.1.7 on 2023-03-09 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('image_filters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('filter_name', models.CharField(max_length=100)),
                ('original_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_filters.uploadedimages')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
