from rest_framework import serializers
from Inventoryapi.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description',
                  'quantity', 'created_on', 'image_path', 'group', 'user', 'total', 'number_purchased')
        depth = 2

class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description',
                  'quantity', 'created_on', 'image_path', 'group', 'user')


class CreateProductSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(decimal_places=3, max_digits=9)
    description = serializers.CharField()
    quantity = serializers.IntegerField()
    created_on = serializers.DateTimeField()
    image_path = serializers.ImageField()
