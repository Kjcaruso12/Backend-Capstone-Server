from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from Inventoryapi.models import Group
from Inventoryapi.serializers import GroupSerializer, CreateGroupSerializer


class GroupView(ViewSet):

    def list(self, request):
        """Get a list of categories
        """
        groups = Group.objects.annotate(product_count=Count('products'))
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new group"""
        try:
            group = Group.objects.create(
                label=request.data['label']
            )
            serializer = CreateGroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Update a group"""
        try:
            group = Group.objects.get(pk=pk)
            group.label = request.data['label']
            group.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """Delete a group"""
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)