from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 

app_name='accounts'
urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile=<str:pk>', views.show_profile, name='show_profile'),
    path('analytics', views.AnalyticsView.as_view(), name='analytics'),
    path('api/data', views.get_data, name='api_data'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('creator_terms', views.CreatorTermsView.as_view(), name='creator_terms'),
    path('new_manga_form', views.NewMangaFormView.as_view(), name='new_manga_form'),
    path('new_chapter_form/<str:pk>', views.NewChapterFormView.as_view(), name='new_chapter_form'),
    path('new_oneshot_form', views.NewOneShotFormView.as_view(), name='new_oneshot_form'),
    path('edit_manga_form/<str:pk>', views.EditMangaFormView.as_view(), name='edit_manga_form'),
    path('edit_chapter_form/<str:pk>', views.EditChapterFormView.as_view(), name='edit_chapter_form'),
    path('edit_oneshot_form/<str:pk>', views.EditOneShotFormView.as_view(), name='edit_oneshot_form'),
    path('coins', views.BuyCoinsView.as_view(), name='buy_coins'),
    path('coins/offer=<int:pk>', views.buy_coins, name='buy_coins'),
    path('coins/process_order', views.process_order, name='process_order'),
    path('withdraw_order', views.WithdrawOrderView.as_view(), name='withdraw_order'),

    #Django Auth
    path('login', views.log_in, name='login'),
    # path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('signup', views.sign_up, name='signup'),
    path('registration_done', views.registration_done, name='registration_done'),
    path('activate_account/<uidb64>/<token>', views.activate_account, name='activate_account')
]