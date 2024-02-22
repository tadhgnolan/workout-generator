from django.db import models

class Donation(models.Model):
    name = models.CharField(max_length=2555, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=5.00) # €5 fixed amount
    stripe_product_id = models.CharField(max_length=255, unique=True) # Store Stripe Product ID
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
