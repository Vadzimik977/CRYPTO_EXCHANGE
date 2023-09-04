from django.forms import ModelForm, ValidationError
from .models import Product
from django import forms

class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {'title': 'Название товара'}

    def price_check(self):
        price = self.cleaned_data['price']

        if not price.isnum():
            raise ValidationError(_('Цена не числом!'))

        return price