from django.urls import path


from . import views 

app_name='public'
urlpatterns = [
    
    path('',views.index, name='index'),
    path('popular',views.popular, name='popular'),
    path('genre',views.genre, name='genre'),

    #Genre URLs
    path('genre/action',views.action, name='action'),
    path('genre/drama',views.drama, name='drama'),
    path('genre/comedy',views.comedy, name='comedy'),
    path('genre/fantasy',views.fantasy, name='fantasy'),
    path('genre/slice_of_life',views.slice_of_life, name='slice_of_life'),
    path('genre/romance',views.romance, name='romance'),
    path('genre/superhero',views.superhero, name='superhero'),
    path('genre/sci-fi',views.sci_fi, name='sci-fi'),
    path('genre/thriller',views.thriller, name='thriller'),
    path('genre/supernatural',views.supernatural, name='supernatural'),
    path('genre/mystery',views.mystery, name='mystery'),
    path('genre/sports',views.sports, name='sports'),
    path('genre/historical',views.historical, name='historical'),
    path('genre/heartwarming',views.heartwarming, name='heartwarming'),
    path('genre/horror',views.horror, name='horror'),
    path('genre/informative',views.informative, name='informative'),

    #Footer URLs
    path('about',views.about, name='about'),
    path('creator_terms',views.creator_terms, name='creator_terms'),
    #path('help',views.help, name='help'),
    path('user_terms',views.user_terms, name='user_terms'),
    path('privacy_policy',views.privacy_policy, name='privacy_policy'),

    path('chapterlist/<str:pk>', views.chapterlist, name='chapterlist'),
    path('chapter_viewer/<str:pk>', views.chapter_viewer, name='chapter_viewer'),
    path('search',views.search, name='search'),
]