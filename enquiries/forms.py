from django import forms
from .models import Enquiry


class EnquiryAddForm(forms.ModelForm):

    class Meta:
        model = Enquiry
        fields = ("email", 'message')
