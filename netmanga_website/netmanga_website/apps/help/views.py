import bleach
from django import template
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth.models import User

from netmanga_website import settings
from .forms import ContactForm

def help(request):
    template = loader.get_template('footer/help.html')
    if request.method == 'GET':
            form = ContactForm(initial={"username": request.user.username, "email": request.user.email})
            #TODO Autofill Username and Email of logged in User in help
            return HttpResponse(template.render({'form': form}, request))
    elif request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = bleach.clean(form.cleaned_data["username"])
            email = bleach.clean(form.cleaned_data["email"])
            message = bleach.clean(form.cleaned_data["message"])

            send_mail(f'{name} with {email} sent an email', message, email, [settings.DEFAULT_FROM_EMAIL])
             
            return HttpResponse(template.render({'form': ContactForm(initial={"username": request.user.username, "email": request.user.email}), 'success': True}, request))
    else:
        raise NotImplementedError

    