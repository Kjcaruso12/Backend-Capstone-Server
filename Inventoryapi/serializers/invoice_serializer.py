from rest_framework import serializers
from Inventoryapi.models import Invoice
from Inventoryapi.serializers import OrderSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ('id', 'invoiceDate', 'total', 'inventoryUser', 'order')
        depth = 2

class CreateInvoiceSerializer(serializers.Serializer):
    invoiceDate = serializers.DateTimeField()
    total = serializers.DecimalField(decimal_places=2, max_digits=9)