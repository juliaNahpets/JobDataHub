from django.contrib import messages
from job_db.models import JobAdvertisement
from job_db.utils import get_job_data_and_write_to_db


def save_dict_to_database(request, data):
    if isinstance(data, list):
        for entry in data:
            proccess_data(request, entry)
    else:
        proccess_data(request, data)


def check_platform_key(data):
    if not data.get("platform"):
        message = "Platform not supported"
        return False, message
    elif not data.get("content"):
        message = f"Only content scraping is supported for {data['platform']}"
        return False, message
    else:
        message = "Data processed successfully!"
        return True, message


def proccess_data(request, entry):
    platform_check, message = check_platform_key(entry)
    if platform_check:
        save_data(request, entry, message)
    else:
        messages.warning(request, message)


def save_data(request, entry, message):
    url_name = entry["url"]
    try:
        job_entry_exists = JobAdvertisement.objects.get(link=url_name)

        if job_entry_exists:
            messages.warning(request, f"An entry for {url_name} already exists.")

    except JobAdvertisement.DoesNotExist:
        messages.success(request, message)
        get_job_data_and_write_to_db(entry)
