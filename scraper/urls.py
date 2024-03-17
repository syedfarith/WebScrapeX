from django.urls import path
from .views import scrape_site,download_content_html,download_content_txt

urlpatterns = [
    path('', scrape_site, name='scrape_site'),
    path('download_html/', download_content_html, name='download_content_html'),    
    path('download_txt/', download_content_txt, name='download_content_txt'), 

]