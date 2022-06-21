from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from Inventoryapi.models import InventoryUser
from Inventoryapi.serializers import UserSerializer


class ProfileView(ViewSet):

    @action(methods=['GET'], detail=False, url_path="my-profile")
    def my_profile(self, request):
        """Get the current user's profile"""
        try:
            user = request.auth.user
            inventoryUser = InventoryUser.objects.get(user=user)
            serializer = UserSerializer(inventoryUser)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['PUT'], detail=False)
    def edit(self, request):
        """Edit the current user's profile"""
        user = request.auth.user
        user.username = request.data['username']
        if request.data.get('password', None):
            user.set_password(request.data['password'])
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)