import uuid
import datetime
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
#{
#    "id": "string",
#    "type": "credit",
#    "amount": 0,
#    "effectiveDate": "2020-10-26T00:50:42.857Z"
#  }


_transaction_list = {}


TRANSACTION_CHOICES = (
    ('debit', 'debit'),
    ('credit', 'credit')
)


def get_current_balance():
    return sum([t.amount if t.transaction_type == 'credit' else (t.amount * -1) 
    for t in _transaction_list.values()])


def get_ordered_transactions():
    return sorted(_transaction_list.values(), key= lambda x:x.effective_date)


class Transaction(object):
    def __init__(self, transaction_type, amount, transaction_id=None, effective_date=None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.transaction_id = transaction_id or uuid.uuid4()
        self.effective_date = effective_date or datetime.datetime.now()
        

class TransactionSerializer(serializers.Serializer):
    id = serializers.UUIDField(source='transaction_id', format='hex_verbose', required=False, read_only=True)
    type = serializers.ChoiceField(source='transaction_type', choices=TRANSACTION_CHOICES)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    effective_date = serializers.DateTimeField(required=False, read_only=True)


class TransactionList(APIView):
    def get(self, request, format=None):
        serializer = TransactionSerializer(_transaction_list.values(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = Transaction(**serializer.validated_data)
            balance = get_current_balance()

            if transaction.transaction_type == 'debit' and balance - transaction.amount < 0:
                return Response('Account balance cannot be negative', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            #No lock necessary, ref:
            #https://docs.python.org/3/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
            _transaction_list[transaction.transaction_id] = transaction
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TransactionDetail(APIView):
    def get(self, request, pk, format=None):
        if pk is None:
            return Response('invalid ID supplied', status=status.HTTP_404_NOT_FOUND)
        if not pk in _transaction_list:
            return Response(status=status.HTTP_404_NOT_FOUND)
        transaction = _transaction_list[pk]
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)


class AccountBalance(APIView):
    def get(self, request, format=None):
        return Response({'balance': get_current_balance()})


class HomeView(TemplateView):
    template_name = 'myapp/home.html'
    def get_context_data(self, **kwargs):
        return {
            'transactions': get_ordered_transactions(),
            'balance': get_current_balance()
        }