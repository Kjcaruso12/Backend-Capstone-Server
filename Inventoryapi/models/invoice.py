from django.db import models

class Invoice(models.Model):
    inventoryUser = models.ForeignKey("InventoryUser", on_delete=models.CASCADE, related_name='inventoryuser')
    order = models.OneToOneField("Order", on_delete=models.CASCADE)
    invoiceDate = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def number_purchased(self):
        return self.__number_purchased

    @number_purchased.setter
    def number_purchased(self,value):
        self.__number_purchased = value