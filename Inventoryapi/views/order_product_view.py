from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from Inventoryapi.models import InventoryUser, Order, OrderProduct
from Inventoryapi.serializers import OrderProductSerializer


class OrderProductView(ViewSet):

    def list(self, request):
        """Get a list of all products"""
        user = InventoryUser.objects.get(user=request.auth.user)
        order = Order.objects.get(user=user, completed_on=None)
        order_products = OrderProduct.objects.filter(order=order)
        serializer = OrderProductSerializer(order_products, many=True)
        return Response(serializer.data)