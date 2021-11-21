from django import forms

from ..accounts.models import Comment, Mangaseries, Award, Profile, ReportChapter

class CommentForm(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Enter Comment'}))

    class Meta:
        model = Comment
        fields = ('comment',)

class EditPlotForm(forms.ModelForm):
    plot = forms.CharField(
        required= True, 
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control', 
                'placeholder': 'Message', 
                'rows': 10
            }
        )
    )
    class Meta:
        model = Mangaseries
        fields = ('plot',)

class ReportForm(forms.ModelForm):
    report = forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Enter Message',
                'rows' : 8,
            }
        )
    )
    class Meta:
        model = ReportChapter
        fields = ('report',)