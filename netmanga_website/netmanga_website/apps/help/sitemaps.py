from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class HelpViewSitemap(Sitemap):

    def items(self):
        return ['help:help']

    def location(self, item):
        return reverse(item)
