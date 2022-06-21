from rest_framework import serializers
from Inventoryapi.models import OrderProduct
from Inventoryapi.serializers import OrderSerializer, ProductSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False)
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'quantity', 'total')
        depth = 2

class CreateOrderProductSerializer(serializers.Serializer):
     quantity = serializers.IntegerField()