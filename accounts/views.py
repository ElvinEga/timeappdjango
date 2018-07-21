from accounts.models import Account, Transaction

import decimal

__all__ = ['view_transactions', 'view_account_by_user_id', 'send_money', 'view_accounts']

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from users.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from pusher_push_notifications import PushNotifications


# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_transactions(request):
    trans = Transaction.objects.all()
    if not trans:
        return Response([])

    data = []
    for transaction in trans:
        transaction_details = {}
        transaction_details['id'] = transaction.id
        # transaction_details['transaction'] = transaction.transact_account
        transaction_details['sender'] = transaction.sender
        transaction_details['receiver'] = transaction.receiver
        transaction_details['amount'] = transaction.amount
        transaction_details['date'] = transaction.date_added

        data.append(transaction_details)

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def view_accounts(request):
    accs = Account.objects.all()
    if not accs:
        return Response([])

    data = []
    for account in accs:
        account_details = {}
        account_details['id'] = account.id
        # account_details['account'] = account.transact_account
        # account_details['user'] = account.user_id()
        account_details['balance'] = account.balance
        account_details['date'] = account.date_modified

        data.append(account_details)

    return Response(data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def view_account_by_user_id(request, user_id):
    try:
        accs = Account.objects.filter(user=user_id)
        data = []
        transaction_details = {}
        account_details = {}
        for account in accs:

            account_details['account_id'] = account.id
            # account_details['user_id'] = account.user_id()

            ac = Account.objects.filter(id=account.id)

            trans = Transaction.objects.filter(account_id=ac)
            tran_data = []

            for transaction in trans:
                transaction_details['id'] = transaction.id
                transaction_details['transact'] = transaction.transact_account
                transaction_details['sender'] = transaction.sender
                transaction_details['receiver'] = transaction.receiver
                transaction_details['amount'] = transaction.amount
                transaction_details['date'] = transaction.date_modified

                tran_data.append(transaction_details)
            account_details['transactions'] = tran_data

        data.append(account_details)

        return Response(data)
    except ObjectDoesNotExist:
        return Response({'error': "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def send_money(request):
    request_details = request.data
    try:
        amount = decimal.Decimal(request_details['amount'])
        sender = User.objects.get(email=request_details['sender'])
        receiver = User.objects.get(email=request_details['receiver'])
    except ObjectDoesNotExist:
        return Response({'error': 'Account Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

    # sender Account deducted
    sender_acc = Account.objects.get(user=sender)
    if sender_acc.balance > amount and sender_acc.balance != 0.00:

        sender_balance = sender_acc.balance - amount
        sender_acc.balance = sender_balance
        sender_acc.save()

        # receiver Account added
        receiver_acc = Account.objects.get(user=receiver)
        receiver_balance = receiver_acc.balance + amount
        receiver_acc.balance = receiver_balance
        receiver_acc.save()

        # Add transaction
        tran = Transaction(
            transact_account=sender_acc,
            sender=sender.email,
            receiver=receiver.email,
            amount=amount,
            transaction_type="send"
        )
        tran.save()

        push_notify("Wallet Transaction successful", str("Transfer cash of Ksh " + str(amount) + " From " +
                                                         str(sender.email) + " To " + str(receiver.email)))
        return Response({'success': "Transaction successful"})
    else:
        return Response({'error': "You have insufficient Amount in account to complete the transaction"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response(eval_details, status=status.HTTP_201_CREATED)


def push_notify(title, message):

    pn_client = PushNotifications(
        instance_id='3ab849d3-463b-4bea-b81e-86b25542a590',
        secret_key='C2C5AA3DEBBA3C415AF5FA21404A654',
    )
    response = pn_client.publish(
        interests=['hello'],
        publish_body={'apns': {'aps': {'alert': 'Transaction'}},
                      'fcm': {'notification': {'title': str(title), 'body': str(message)}}}
    )

    print(response['publishId'])

