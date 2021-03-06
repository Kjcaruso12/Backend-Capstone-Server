from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from Inventoryapi.models import Order, Invoice, InventoryUser
from Inventoryapi.models.order_product import OrderProduct
from Inventoryapi.serializers import InvoiceSerializer, CreateInvoiceSerializer


class InvoiceView(ViewSet):

    def create(self, request):
        """Create a new invoice for the current order"""
        user = InventoryUser.objects.get(user=request.auth.user)
        order = Order.objects.get(pk=request.data['order_id'])
        order_products = OrderProduct.objects.filter(order=order)
        total = 0
        for order_product in order_products:
            total += order_product.total
        try:
            invoice = Invoice.objects.create(
                total=total,
                order=order,
                inventoryUser=user
            )
            serializer = CreateInvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Get a single Invoice"""
        try:
            invoice = Invoice.objects.filter(pk=pk)
            order = Order. objects.get(pk=invoice.order_id)
            invoice.order = order
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get a list of the current users orders
        """
        invoices = Invoice.objects.all()
        for invoice in invoices:
            order = Order.objects.get(pk=invoice.order_id)
            order_products = OrderProduct.objects.filter(order=order)
            total = sum([p.quantity for p in order_products], 0)
            invoice.number_purchased = total
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)


    def destroy(self, request, pk):
        """Delete an order, current user must be associated with the order to be deleted
        """
        try:
            invoice = Invoice.objects.get(pk=pk)
            invoice.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
