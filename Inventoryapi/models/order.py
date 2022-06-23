from django.db import models
from Inventoryapi.models import InventoryUser

class Order(models.Model):
    user = models.ForeignKey(InventoryUser, on_delete=models.CASCADE, related_name="order")
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    products = models.ManyToManyField("Product", through="OrderProduct", related_name="orders")

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self,value):
        self.__total = value

    # @property
    # def number_purchased(self):
    #     """Calculates total quantity of products in an order
    #     Returns:
    #         integer: The sum of the product quantities on the order
    #     """
    #     return sum([p.quantity for p in self.products.all()], 0)