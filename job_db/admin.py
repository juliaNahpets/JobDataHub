from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . import models

# Register your models here.


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "website", "get_branches")

    def get_branches(self, obj):
        return ", ".join([branch.name for branch in obj.branch.all()])

    get_branches.short_description = "branch"


@admin.register(models.JobAdvertisement)
class JobAdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_link",
        "job_title",
        "date_scraped",
        "direct_apply",
        "get_employment_types",
        "get_locations",
        "home_office",
        "get_company_link",
        "get_qualifications",
    )

    def get_link(self, obj):
        url = reverse("admin:job_db_jobadvertisement_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.link)

    get_link.short_description = "Link"

    def get_company_link(self, obj):
        if obj.company:
            url = reverse("admin:job_db_company_change", args=[obj.company.id])
            return format_html('<a href="{}">{}</a>', url, obj.company.name)
        return "-"

    get_company_link.short_description = "Company"

    def get_employment_types(self, obj):
        return ", ".join([et.name for et in obj.employment_type.all()])

    get_employment_types.short_description = "employment type"

    def get_locations(self, obj):
        return ", ".join([loc.name for loc in obj.location.all()])

    get_locations.short_description = "location"

    def get_qualifications(self, obj):
        return ", ".join([q.name for q in obj.qualification.all()])

    get_qualifications.short_description = "qualification"
