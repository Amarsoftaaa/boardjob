from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Job


class JobSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Job.objects.filter(is_active=True).order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("job_detail", kwargs={"slug": obj.slug, "pk": obj.pk})


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ["home", "job_list"]

    def location(self, item):
        return reverse(item)
