# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-22 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
                ('course_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courses.Course')),
            ],
            bases=('courses.course',),
        ),
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u8f6e\u64ad'),
        ),
    ]
