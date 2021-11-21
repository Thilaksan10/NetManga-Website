from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import Profile, Creator, Mangaseries, Chapter, Chapterimages, Rating
from .choices import GENRE_CHOICES

class SignUpForm(UserCreationForm):
   username = forms.CharField(
      required=True, 
      widget=forms.TextInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Username*'
            }
         )
      )

   first_name = forms.CharField(
      max_length=30, 
      required=True, 
      widget=forms.TextInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter First Name (Optional)'
            }
         )
      )

   last_name = forms.CharField(
      max_length=30, 
      required=True, 
      widget=forms.TextInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Last Name (Optional)'
            }
         )
      )

   birth_date = forms.DateField(
      required=True, 
      widget=forms.DateInput(
         attrs={
            'class' : 'form-control', 
            'placeholder' : 'Enter Birth Date (YYYY-MM-DD)*'
            }
         )
      )

   email = forms.EmailField(
      required=True, 
      widget=forms.EmailInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Email Address*'
            }
         )
      )

   password1 = forms.CharField(
      required=True, 
      min_length=8, 
      max_length=20, 
      label='Password', 
      widget=forms.PasswordInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Password*'
            }
         )
      )

   password2 = forms.CharField(
      required=True, 
      min_length=8, 
      max_length=20, 
      label='Password Confirmation', 
      widget=forms.PasswordInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Confirm Password*'
            }
         )
      )

   advertise_consent = forms.BooleanField(
      required=False, 
      label='Consent to Netmanga Advertising and Marketing', 
      label_suffix='', 
      help_text='I agree to receive service updates, news and events form NETMANGA by email.', 
      widget=forms.CheckboxInput(
         attrs={
            'class' : 'checkbox'
            }
         )
      )


   terms_consent = forms.BooleanField(
      required=True, 
      label='Terms of Use and Privacy Policy*', 
      label_suffix='',
      help_text='', 
      widget=forms.CheckboxInput(
         attrs={
            'class' : 'checkbox' 
            }
         )
      )

   class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'birth_date', 'email', 'password1', 'password2',
         'advertise_consent', 'terms_consent')

class LoginForm(forms.Form):
   username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter Username'}))
   password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Enter Password'}))

class EditProfileForm(forms.ModelForm):
   profile_Picture = forms.ImageField(
      required=False,
      widget=forms.FileInput(
         attrs={
            'class': 'form-control',
         }
      )
   )

   display_Full_Name = forms.BooleanField(
      required=False, 
      label='Display Full Name', 
      label_suffix='', 
      widget=forms.CheckboxInput(
         attrs={
            'class' : 'checkbox'
            }
         )
      )

   bio = forms.CharField(
      required= True, 
      max_length=500,
      widget=forms.Textarea(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Message', 
            'rows': 5
         }
      )
   )

   class Meta:
      model = Profile
      fields = ('profile_Picture','bio','display_Full_Name')

class CreatorForm(forms.ModelForm):

   terms_consent = forms.BooleanField(
      required=True, 
      label='Terms of Use and Privacy Policy*', 
      label_suffix='',
      help_text='', 
      widget=forms.CheckboxInput(
         attrs={
            'class' : 'checkbox' 
            }
         )
      )

   class Meta:
      model = Creator
      fields = ('terms_consent',)


class MangaForm(forms.ModelForm):
   
   title = forms.CharField(
      required=True, 
      max_length=100,
      widget=forms.TextInput(
         attrs={
            'class': 'form-control',
            'placeholder' : 'Enter Manga Title',
            }
         )
      )

   cover_picture = forms.ImageField(
      required=True,
      widget=forms.FileInput(
         attrs={
            'class': 'form-control',
         }
      )
   )

   plot = forms.CharField(
      required=True, 
      widget=forms.Textarea(
         attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Manga Plot', 
            'rows': 7
            }
         )
      )


   primary_Genre = forms.ChoiceField(
         required=True,
         choices=GENRE_CHOICES,
      )

   secondary_Genre = forms.ChoiceField(
         required=True,
         choices=GENRE_CHOICES,
      )

   class Meta:
      model = Mangaseries
      fields = ('cover_picture','title','primary_Genre','secondary_Genre','plot')

class EditMangaForm(forms.ModelForm):
   
   title = forms.CharField(
      required=True, 
      max_length=100, 
      widget=forms.TextInput(
         attrs={
            'class': 'form-control',
            'placeholder' : 'Edit Manga Title',
            }
         )
      )

   cover_picture = forms.ImageField(
      required=False,
      widget=forms.FileInput(
         attrs={
            'class': 'form-control',
         }
      )
   )

   plot = forms.CharField(
      required=True, 
      widget=forms.Textarea(
         attrs={
            'class': 'form-control',
            'placeholder': 'Edit the Manga Plot', 
            'rows': 7
            }
         )
      )


   primary_Genre = forms.ChoiceField(
         required=True,
         choices=GENRE_CHOICES,
      )

   secondary_Genre = forms.ChoiceField(
         required=True,
         choices=GENRE_CHOICES,
      )

   class Meta:
      model = Mangaseries
      fields = ('cover_picture','title','primary_Genre','secondary_Genre','plot')


class ChapterForm(forms.ModelForm):

   title = forms.CharField(
      max_length=100,
      required=True,
      widget=forms.TextInput(
         attrs={
            'class': 'form-control',
            'placeholder': 'Enter the Chapter Title'
         }
      )
   )
   class Meta:
      model = Chapter
      fields = ('title',)

class ResetPasswordForm(PasswordResetForm):

   email = forms.EmailField(
      required=True, 
      widget=forms.EmailInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Email Address'
            }
         )
      )

class ChangePasswordForm(SetPasswordForm):

   new_password1 = forms.CharField(
      required=True, 
      min_length=8, 
      max_length=20, 
      label='Password', 
      widget=forms.PasswordInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Enter Password*'
            }
         )
      )

   new_password2 = forms.CharField(
      required=True, 
      min_length=8, 
      max_length=20, 
      label='Password Confirmation', 
      widget=forms.PasswordInput(
         attrs={
            'class' : 'form-control', 
            'placeholder': 'Confirm Password*'
            }
         )
      )