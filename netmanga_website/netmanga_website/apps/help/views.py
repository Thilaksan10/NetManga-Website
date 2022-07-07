from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail
from ..accounts.models import User
from django.utils.html import strip_tags

from netmanga_website import settings
from .forms import ContactForm
from .models import Issue
from ..accounts.models import User

def help(request):
    template = loader.get_template('footer/help.html')
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = ContactForm(initial={"email": request.user.email})
        else:
            form = ContactForm()
        return HttpResponse(template.render({'form': form}, request))
    elif request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            user = User.objects.filter(email=email).first()
            if user:
                priority = 2
            else:
                priority = 0
            issue = Issue.objects.create(email=email, message=message, status='Reviewing', priority=priority)
            issue.save()
            subject = f'NetManga Issue ID: {issue.pk}'
            email_template_name = 'footer/contact_review_mail.html'
            parameters = {
                'email' : email,
                'issue' : issue,
                'site_name' : 'NetManga',
            }
            html_message = loader.render_to_string(email_template_name, parameters)
            plain_message = strip_tags(message)
            send_mail(subject, plain_message , '', [email], html_message=html_message, fail_silently=False)
             
            return HttpResponse(template.render({'form': ContactForm(initial={"email": email}), 'success': True}, request))
        return HttpResponse(template.render({'form': ContactForm(), 'success': False}, request))
    else:
        raise NotImplementedError

    