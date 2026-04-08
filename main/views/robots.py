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
        "Disallow: /api/",
        "Disallow: /form/",
        "Disallow: /media/",
        "Allow: /static/main/css/",
        "Allow: /static/main/js/",
        "Allow: /static/main/media/",
        "Allow: /static/main/documents/",
        "Allow: /",
        "",
        "# Yandex-specific directives",
        "User-agent: Yandex",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /form/",
        "Disallow: /media/",
        "Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term",
        "Clean-param: yclid&gclid&fbclid",
        "",
        f"Host: https://{request.get_host()}",
        f"Sitemap: https://{request.get_host()}{reverse('sitemap')}",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")
