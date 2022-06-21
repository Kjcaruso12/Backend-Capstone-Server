from rest_framework import serializers
from Inventoryapi.models import Group


class GroupSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(default=None)

    class Meta:
        model = Group
        fields = ('id', 'created_on', 'label', 'product_count')
        depth = 1

class CreateGroupSerializer(serializers.Serializer):
    created_on = serializers.DateTimeField()
    label = serializers.CharField()