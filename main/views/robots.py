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
        "Disallow: /media/",
        "Disallow: /*?",
        "Disallow: /*&",
        "Allow: /static/main/css/",
        "Allow: /static/main/js/",
        "Allow: /static/main/media/",
        "Allow: /static/main/documents/",
        "Allow: /",
        f"Sitemap: {request.scheme}://{request.get_host()}{reverse('sitemap')}",
        f"Host: {request.get_host()}",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
