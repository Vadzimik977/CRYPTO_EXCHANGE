from django.contrib import admin
from .models import  Product, ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
# Register your models here.
