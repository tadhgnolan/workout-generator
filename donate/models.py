from django.db import models

class Donation(models.Model):
    order_number = models.CharField(max_length=2555, unique=True)
    email = models.EmailField(max_length=254, null=False, blank=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=5.00) # €5 fixed amount
    stripe_product_id = models.CharField(max_length=255, unique=True) # Store Stripe Product ID
    date = models.DateTimeField(auto_now_add=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
