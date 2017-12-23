# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 21:01
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('object_pk', models.CharField(default='', max_length=255, verbose_name='object ID')),
                ('text', models.TextField(validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='text')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ct_set_for_comment', to='contenttypes.ContentType', verbose_name='content type')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comment.Comment', verbose_name='parent comment')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['date_created'],
            },
        ),
    ]
