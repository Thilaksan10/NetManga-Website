from django import forms
from ..accounts.models import User

class ContactForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Email'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Message', 'rows': 4}))

    class Meta:
        model = User
        fields = ('email', 'message')
