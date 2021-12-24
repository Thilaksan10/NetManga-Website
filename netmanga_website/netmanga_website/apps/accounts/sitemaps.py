from django.contrib.sitemaps import Sitemap

from .models import MangaSeries, Chapter, OneShot, Profile

class MangaSeriesSitemap(Sitemap):

    def items(self):
        return MangaSeries.objects.all().order_by('pk')

    
class ChapterSitemap(Sitemap):

    def items(self):
        return Chapter.objects.all().order_by('published')

class OneshotSitemap(Sitemap):

    def items(self):
        return OneShot.objects.all().order_by('published')

class ProfileSitemap(Sitemap):
    
    def items(self):
        return Profile.objects.all().order_by('pk')