from . import models
from webScraping.main import webscraping


def get_job_data_and_write_to_db(raw_content):
    job_data = webscraping(raw_content)
    write_job_dict_to_db(job_data)


def write_job_dict_to_db(dic):
    company_name = dic["companyInfos"]["name"]
    location_name = dic["companyInfos"]["location"] or None

    company_location, _ = (
        models.Location.objects.get_or_create(name=location_name)
        if location_name
        else (None, None)
    )

    try:
        company_exists = models.Company.objects.get(name=company_name)

        if company_exists.location != company_location:
            company_exists.location = company_location
            company_exists.save()

        company = company_exists

    except models.Company.DoesNotExist:
        company = models.Company.objects.create(
            name=company_name,
            location=company_location,
            website=dic["companyInfos"]["website"],
        )

    company_branches = process_comma_separated(dic["companyInfos"]["branch"])

    if company_branches:
        company.branch.add(
            *[
                models.Branch.objects.get_or_create(name=branch_name)[0]
                for branch_name in company_branches
            ]
        )

    job_advertisement, _ = models.JobAdvertisement.objects.update_or_create(
        link=dic["jobLink"],
        defaults={
            "job_title": dic["jobTitle"],
            "direct_apply": dic["directApply"],
            "home_office": dic["homeOffice"],
            "company": company,
            "job_description": dic["jobDescription"] or None,
        },
    )

    if dic["qualifications"]:
        job_advertisement.qualification.add(
            *[
                models.Qualification.objects.get_or_create(name=qualification_name)[0]
                for qualification_name in dic["qualifications"]
            ]
        )

    job_locations = process_comma_separated(dic["jobLocation"])

    if job_locations:
        job_advertisement.location.add(
            *[
                models.Location.objects.get_or_create(name=location_name)[0]
                for location_name in job_locations
            ]
        )

    employment_types = process_comma_separated(dic["employmentType"])

    if employment_types:
        job_advertisement.employment_type.add(
            *[
                models.EmploymentType.objects.get_or_create(name=emp_type)[0]
                for emp_type in employment_types
            ]
        )


def process_comma_separated(value):
    if not value or value == "":
        return None
    else:
        return [item.strip() for item in value.split(",")] if "," in value else [value]
