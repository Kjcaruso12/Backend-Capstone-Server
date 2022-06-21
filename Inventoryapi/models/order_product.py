from django.db import models


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total(self):
        total_amount = 0
        total_amount += (self.quantity * self.product.price)
        return total_amount
