from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):

    def items(self):
        return ['public:index', 'public:popular', 'public:genre', 'public:action', 'public:drama', 'public:comedy', 'public:fantasy', 'public:slice_of_life', 'public:romance', 'public:superhero', 'public:sci-fi', 'public:thriller', 'public:supernatural', 'public:mystery', 'public:sports', 'public:historical', 'public:heartwarming', 'public:horror', 'public:informative', 'public:about', 'public:creator_terms', 'public:user_terms', 'public:privacy_policy']

    def location(self, item):
        return reverse(item)
