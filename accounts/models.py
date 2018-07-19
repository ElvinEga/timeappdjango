from __future__ import unicode_literals
import uuid


from django.db import models

# Create your models here.
from django.db.models import Q

from users.models import User

TRANSACTIONS = (
    ('receive', 'receive'),
    ('send', 'send'),
)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name="user", limit_choices_to=Q(role='user'),
                                   on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        count = Account.objects.count()
        super(Account, self).save(*args, **kwargs)

    def user_id(self):
        return str(self.user.id)

    def user_email(self):
        return str(self.user.email)

    def __unicode__(self):
        return "%s | %s" % (str(self.id), self.user)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    transact_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=255, unique=False)
    receiver = models.CharField(max_length=255, unique=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTIONS, default='send')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.sender, self.amount)