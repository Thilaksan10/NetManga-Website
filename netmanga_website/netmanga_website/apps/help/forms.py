from django import forms
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Email'}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Message', 'rows': 4}))

    class Meta:
        model = User
        fields = ('name', 'email', 'message')
