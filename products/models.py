from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Product(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    add_date = models.DateField(default=timezone.now)
    add_to_favorites = models.ManyToManyField(User, related_name='user_favourite', blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.price)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)  # Замените Item на вашу модель

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in ProductImage._meta.fields]