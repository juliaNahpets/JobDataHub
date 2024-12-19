from django.shortcuts import render, redirect
from webScraping.main import (
    get_platform,
    get_content_dict_list,
)
from .utils import save_dict_to_database
from . import forms
import json


def index(request):
    return render(request, "job_interface/index.html", {"active_page": "index"})


def url_scraper(request):
    form = forms.UrlScraperForm()
    if request.method == "POST":
        form = forms.UrlScraperForm(request.POST)
        if form.is_valid():
            json_url_list = form.cleaned_data.get("url_list")
            url_list = json.loads(json_url_list)
            dict_list = get_content_dict_list(url_list)
            save_dict_to_database(request, dict_list)
            return redirect("/url-scraper/")
    return render(
        request,
        "job_interface/url_scraper.html",
        {"active_page": "url_scraper", "form": form},
    )


def content_scraper(request):
    form = forms.ContentScraperForm()
    if request.method == "POST":
        form = forms.ContentScraperForm(request.POST)
        if form.is_valid():
            job_data = {
                "url": form.cleaned_data["url"],
                "content": form.cleaned_data["content"],
                "platform": get_platform(form.cleaned_data["url"]),
            }
            save_dict_to_database(request, job_data)
            return redirect("/content-scraper/")
    return render(
        request,
        "job_interface/content_scraper.html",
        {"active_page": "content_scraper", "form": form},
    )


def job_advertisement_db(request):
    return render(
        request,
        "job_interface/job_advertisement_db.html",
        {"active_page": "job_advertisement_db"},
    )
