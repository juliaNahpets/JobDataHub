from django.urls import path
from . import views

urlpatterns = [
    path("api/job-data", views.job_data_api, name="job_data_api"),
    path("api/url-scraper", views.url_scraper_api, name="url_scraper_api"),
    path("api/content-scraper", views.content_scraper_api, name="content_scraper_api"),
]
