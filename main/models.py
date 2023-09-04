from django.db import models
from django.contrib.auth.models import User
class Application(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.amount} {self.currency}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
    )
    order_id = models.AutoField(primary_key=True)
    crypto_currency = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    email = models.EmailField()
    operation_type = models.CharField(max_length=10, default='None')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    processed=models.DecimalField(max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return f"{self.email} - {self.crypto_currency} - {self.amount}"
class OrderComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class OrderRating(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(1, '😢'), (2, '😞'), (3, '😐'), (4, '😊'), (5, '😄')])

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(1, '😢'), (2, '😞'), (3, '😐'), (4, '😊'), (5, '😄')],default=0)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on Order {self.order.order_id}"



# Create your models here.
