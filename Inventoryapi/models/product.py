from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(validators=[
        MinValueValidator(0.00), MaxValueValidator(10000.00)])
    description = models.TextField()
    quantity = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    image_path = models.ImageField(upload_to='products', height_field=None,
                                   width_field=None, max_length=None, null=True, blank=True)
    group = models.ForeignKey(
        "Group", on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(
        "InventoryUser", on_delete=models.CASCADE, related_name='users')


    @property
    def total(self):
        """Returns the total price of the combined quantity
        """
        total_amount = (self.quantity * self.price)
        return total_amount

    @property
    def number_purchased(self):
        """Returns the quantity of product sold
         """
        total = 0
        for product in self.orderproduct_set.all():
            if product.product_id == self.id:
                if product.order.completed_on is not None:
                    total += product.quantity
        return total

