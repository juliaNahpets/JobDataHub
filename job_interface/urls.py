from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("url-scraper/", views.url_scraper, name="url_scraper"),
    path("content-scraper/", views.content_scraper, name="content_scraper"),
    path(
        "job-advertisement-overview/",
        views.job_advertisement_db,
        name="job_advertisement_db",
    ),
]
