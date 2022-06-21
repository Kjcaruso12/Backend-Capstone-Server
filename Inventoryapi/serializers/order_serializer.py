from rest_framework import serializers
from Inventoryapi.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'products', 'created_on', 'completed_on', 'total', 'number_purchased')
        depth = 2

class UpdateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('completed_on',)