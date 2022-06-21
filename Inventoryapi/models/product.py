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
        """Returns the number of times product shows up on completed orders
        """
        total_sold = 0
        for product in self.orders.all():
            total_sold += product.quantity
        return total_sold