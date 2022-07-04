"""netmanga_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, sitemaps
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

from . import views
from .apps.accounts.forms import ResetPasswordForm, ChangePasswordForm
from .apps.public.sitemaps import StaticViewSitemap
from .apps.accounts.sitemaps import MangaSeriesSitemap, OneshotSitemap, ChapterSitemap, ProfileSitemap
from .apps.help.sitemaps import HelpViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'help': HelpViewSitemap,
    'manga_series': MangaSeriesSitemap,
    'one_shot': OneshotSitemap,
    'profile': ProfileSitemap,
    'chapter': ChapterSitemap,
    
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('netmanga_website.apps.public.urls')),
    path('accounts/', include('netmanga_website.apps.accounts.urls')),
    path('help/', include('netmanga_website.apps.help.urls')),
    path('staff/', include('netmanga_website.apps.staff.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Django reset Password
    path('reset_password', auth_views.PasswordResetView.as_view(form_class=ResetPasswordForm, template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(form_class=ChangePasswordForm, template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)