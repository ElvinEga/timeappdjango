from __future__ import unicode_literals

from django.db import models

# Create your models here.


__all__ = ['User']

import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


# Create your models here.
STATUSES = (
    ('100', 'Created'),
    ('200', 'Approved'),
    ('300', 'Rejected'),
)
ROLES = (
    ('user', 'user'),
    ('agent', 'agent'),
    ('admin', 'admin'),
)
"""
 User's table
 statuses:
     - 100: created
     - 200: approved
     - 300: rejected
 """


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=30, choices=ROLES, default='user')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    # Whether user has been approved or rejected
    status = models.CharField(max_length=3, choices=STATUSES, default='100')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        permissions = (
            ('can_disable_users', 'can disable users'),
            ('can_freeze_users', 'can freeze users'),
            #('can_approve_users', 'can approve users'),
            ('can_add_users', 'can add users'),
            ('can_view_users', 'can view users'),
            ('can_view_data', 'can view data'),
            ('evaluate_lecturer', 'evaluate lecturer'),

            ('can_upload_members', 'can upload members'),

        )



    def get_full_name(self):
        '''
	    Returns the first_name plus the last_name, with a space in between.
	    '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
	    Returns the short name for the user.
	    '''
        return self.first_name


    def __unicode__(self):
        """
		Human redeable string representation of a user.
		"""
        return "%s -- %s %s" % (self.email, self.first_name, self.last_name)
        #return str(self.id)

