from rest_framework import serializers
from Inventoryapi.models import InventoryUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryUser
        fields = ('id', 'admin', 'user')
        depth = 1


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()