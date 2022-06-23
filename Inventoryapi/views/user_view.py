from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from Inventoryapi.models import InventoryUser
from Inventoryapi.serializers import UserSerializer


class UserView(ViewSet):

    def list(self, request):
        """Get a list of users
        """
        users = InventoryUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
