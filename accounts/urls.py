from django.conf.urls import url, patterns

from .views import *

urlpatterns = [
    url(r'^send_money/$', send_money),
    url(r'^view_accounts/$', view_accounts),
    url(r'^view_transactions/$', view_transactions),
    url(r'^view_account_by_user_id/(?P<user_id>[0-9a-z-]+)/$', view_account_by_user_id),
    url(r'^view_transactions_by_number/(?P<number>[0-9a-z-]+)/$', view_transactions_by_number)
]
