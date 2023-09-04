from django import forms
from .models import OrderRating, OrderComment

class CurrencyExchangeForm(forms.Form):
    currency_choices = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Etherium'),
        ('SOL', 'Solana'),
        ('TON', 'Ton'),
        # Добавьте другие валюты по необходимости
    ]

    from_currency = forms.ChoiceField(choices=currency_choices)
    amount = forms.DecimalField()
class OrderRatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(1, '😢'), (2, '😞'), (3, '😐'), (4, '😊'), (5, '😄')])

class OrderCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

