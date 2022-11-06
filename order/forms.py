from django import forms
from django.forms import widgets

from core.validators import validate_bd_number

from django_countries.fields import CountryField


class CheckoutForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields['address'].widget.attrs.update({"rows": 5})


    first_name = forms.CharField(
        max_length=60
    )
    last_name = forms.CharField(
        max_length=50
    )
    email = forms.EmailField(
        max_length=100
    )
    phone_number = forms.CharField(
        max_length=13,
        validators=[validate_bd_number]
    )
    city = forms.CharField(
        max_length=50
    )
    zip_code = forms.CharField(
        max_length=8
    )
    country = CountryField().formfield()
    address = forms.CharField(
        widget=forms.Textarea
    )

