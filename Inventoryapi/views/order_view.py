from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from Inventoryapi.models import Order, InventoryUser, OrderProduct
from Inventoryapi.models.product import Product
from Inventoryapi.serializers import OrderSerializer


class OrderView(ViewSet):

    def retrieve(self, request, pk):
        """Get a single Order"""
        try:
            order = Order.objects.filter(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get a list of the current users orders
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    def destroy(self, request, pk):
        """Delete an order, current user must be associated with the order to be deleted
        """
        try:
            user = InventoryUser.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, user=user)
            order.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['put'], detail=True)
    def complete(self, request, pk):
        """Complete an order by adding a payment type and completed data
        """
        try:
            user = InventoryUser.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, user=user)
            products = order.products.all()
            for product in products:
                product_inst = Product.objects.get(pk=product.id)
                order_product = OrderProduct.objects.get(product=product_inst, order=order)
                product_inst.quantity -= order_product.quantity
                product_inst.save()
            order.completed_on = datetime.now()
            order.save()
            return Response({'message': "Order Completed"})
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['get'], detail=False)
    def current(self, request):
        """Get the user's current order"""
        try:
            user = InventoryUser.objects.get(user=request.auth.user)
            order = Order.objects.get(
                completed_on=None, user=user)
            order_products = OrderProduct.objects.filter(order=order)
            total = 0
            for order_product in order_products:
                total += order_product.total
            order.total = total
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({
                'message': 'You do not have an open order. Add a product to the cart to get started'},
                status=status.HTTP_404_NOT_FOUND
            )