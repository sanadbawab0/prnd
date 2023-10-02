from django import forms
from .models import Car, Review


class CarFilterForm(forms.ModelForm):
    brand = forms.CharField(required=False)
    model = forms.CharField(required=False)
    release_year = forms.IntegerField(required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)

    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'body_type', 'release_year',
            'transmission_type', 'fuel_type', 'color',
            'condition', 'custom',
        ]
