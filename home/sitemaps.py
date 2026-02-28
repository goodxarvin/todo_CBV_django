from django.contrib.sitemaps import Sitemap
from .models import Objective

class ObjectiveSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Objective.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at

# this page is not that practical but i just created it just in case