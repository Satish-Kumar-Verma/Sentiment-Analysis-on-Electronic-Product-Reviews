from django import forms
from .models import Contact

class DataExtractionForm(forms.Form):
    reviews_link = forms.URLField(label='Reviews Link', required=True)
    num_pages = forms.IntegerField(label='No. of pages', required=True, min_value=1)
    spec_link = forms.URLField(label='Specifications Link', required=True)
    product_type = forms.CharField(label='Product Type', required=True, max_length=100)
    product_brand = forms.CharField(label='Product Brand', required=True, max_length=100)
    product_model = forms.CharField(label='Product Model', required=True, max_length=100)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
