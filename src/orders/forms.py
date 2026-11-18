from django import forms

from catalog.models import Product


class OrderCreateForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True))
    quantity = forms.IntegerField(min_value=1, initial=1)
