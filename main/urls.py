from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import SitemapRegistry


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('form/', views.send_contacts, name='send_contacts'),
    path('catalog/', views.Catalog.as_view(), name='catalog'),
    path('about/', views.About.as_view(), name='about'),
    path('about/certificates/', views.Certificates.as_view(), name='certificates'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('delivery/', views.Delivery.as_view(), name='delivery'),
    path('complete_projects/', views.CompleteProjects.as_view(), name='complete_projects'),
    path('services/', views.Services.as_view(), name='services'),
    path('services/<slug:service_slug>/', views.Service.as_view(), name='service'),
    path('category/<slug:category_slug>/', views.Category.as_view(), name='category'),
    path('product/<slug:product_slug>/', views.Product.as_view(), name='product'),

    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': SitemapRegistry.get_sitemaps()}, name='sitemap'),
]

api_urlpatterns = [
    path('send_contacts/', views.send_contacts, name='send_contacts_api'),
    path('products/', views.get_products, name='get_products'),
]

urlpatterns += [path('api/', include((api_urlpatterns, 'api')))]


