from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    """
    Generates a robots.txt file for the site.
    This file is used to control how search engines index the site.
    """
    content = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /static/",
        "Disallow: /media/",
        "Disallow: /*?",
        "Disallow: /*&",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}{reverse('sitemap')}",
        f"Host: {request.get_host()}",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
