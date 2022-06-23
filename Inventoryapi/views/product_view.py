from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from Inventoryapi.models import InventoryUser, Group, Product, Order, OrderProduct
from Inventoryapi.serializers import ProductSerializer, CreateProductSerializer, CreateOrderProductSerializer


class ProductView(ViewSet):

    def create(self, request):
        """Create a new product for the current user's store"""
        user = InventoryUser.objects.get(user=request.auth.user)
        group = Group.objects.get(pk=request.data['group_id'])
        try:
            product = Product.objects.create(
                name=request.data['name'],
                price=request.data['price'],
                description=request.data['description'],
                quantity=request.data['quantity'],
                image_path=request.data['image_path'],
                group=group,
                user=user
            )
            serializer = CreateProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        """Update a product"""
        group = Group.objects.get(pk=request.data['group_id'])

        try:
            product = Product.objects.get(pk=pk)
            product.name = request.data['name']
            product.price = request.data['price']
            product.description = request.data['description']
            product.quantity = request.data['quantity']
            product.image_path = request.data['image_path']
            product.group = group
            product.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk):
        """Delete a product"""
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Get a list of all products"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk):
        """Get a single product"""
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['post'], detail=True)
    def add_to_order(self, request, pk):
        """Add a product to the current users open order"""
        try:
            user = InventoryUser.objects.get(user=request.auth.user)
            product = Product.objects.get(pk=pk)
            order, _ = Order.objects.get_or_create(
                user=user, completed_on=None)
            order.products.add(product, through_defaults={'quantity': request.data['quantity']})
            # Update so that when a product gets added thats already in the order, its puts a put request to update the quantity instead of adding a new product
            return Response({'message': 'product added'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['delete'], detail=True)
    def remove_from_order(self, request, pk):
        """Remove a product from the users open order"""
        try:
            user = InventoryUser.objects.get(user=request.auth.user)
            product = Product.objects.get(pk=pk)
            order = Order.objects.get(
                user=user, completed_on=None)
            order_product = OrderProduct.objects.get(order=order.id, product=product.id)
            order.products.remove(product)
            order_product.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except (Product.DoesNotExist, Order.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


