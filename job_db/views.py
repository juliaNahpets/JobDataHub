from .models import JobAdvertisement
from job_interface.utils import save_dict_to_database
from django.contrib import messages
from django.http import JsonResponse
from webScraping.main import get_platform, get_content_dict_list
import json


def url_scraper_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url_list = [data["url"]]
        dict_list = get_content_dict_list(url_list)
        save_dict_to_database(request, dict_list)
        msgs = messages.get_messages(request)
        data["messages"] = [{"lvl": m.level, "msg": m.message} for m in msgs]
        return JsonResponse(data, status=202)
    else:
        return JsonResponse({"message": "Site loaded"}, status=200)


def content_scraper_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data["url"]
        job_data = {
            "url": url,
            "content": data["content"],
            "platform": get_platform(url),
        }
        save_dict_to_database(request, job_data)
        msgs = messages.get_messages(request)
        data["messages"] = [{"lvl": m.level, "msg": m.message} for m in msgs]
        return JsonResponse(data, status=202)
    else:
        return JsonResponse({"message": "Site loaded"}, status=200)


def job_data_api(request):
    jobs = JobAdvertisement.objects.all()
    job_list = []
    for job in jobs:
        job_dict = {
            "id": job.id,
            "link": job.link,
            "job_title": job.job_title,
            "date_scraped": job.date_scraped.strftime("%m %B %Y, %H:%M"),
            "direct_apply": check_status(job.direct_apply),
            "employment_type": join_item(job.employment_type.all()),
            "location": join_item(job.location.all()),
            "home_office": check_status(job.home_office),
            "company": job.company.name,
            "qualification": join_item(job.qualification.all()),
        }
        job_list.append(job_dict)
    return JsonResponse({"data": job_list}, safe=False)


def check_status(value):
    return (
        '<i class="bi bi-check-circle" style="color: green;"></i>'
        if value
        else '<i class="bi bi-x-circle" style="color: red;"></i>'
    )


def join_item(value):
    return ", ".join([item.name for item in value])
