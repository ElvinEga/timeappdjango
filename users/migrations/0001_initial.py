# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-17 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import users.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('role', models.CharField(choices=[('user', 'user'), ('agent', 'agent'), ('admin', 'admin')], default='user', max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('100', 'Created'), ('200', 'Approved'), ('300', 'Rejected')], default='100', max_length=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'permissions': (('can_disable_users', 'can disable users'), ('can_freeze_users', 'can freeze users'), ('can_add_users', 'can add users'), ('can_view_users', 'can view users'), ('can_view_data', 'can view data'), ('evaluate_lecturer', 'evaluate lecturer'), ('can_upload_members', 'can upload members')),
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]
