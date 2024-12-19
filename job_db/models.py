from django.db import models


class EmploymentType(models.Model):
    name = models.CharField("name", max_length=90, unique=True)

    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
        indexes = [models.Index(fields=["name"], name="employment_type_index")]

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField("name", max_length=90, unique=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        indexes = [models.Index(fields=["name"], name="location_index")]

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField("name", max_length=150, unique=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        indexes = [models.Index(fields=["name"], name="branch_index")]

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField("name", max_length=90, unique=True)

    class Meta:
        verbose_name = "Qualification"
        verbose_name_plural = "qualifications"
        indexes = [models.Index(fields=["name"], name="qualification_index")]

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField("name", max_length=255, db_index=True)

    location = models.ForeignKey(
        Location,
        verbose_name="location",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    branch = models.ManyToManyField(Branch, verbose_name="branch", blank=True)

    website = models.URLField("website", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        indexes = [models.Index(fields=["name"], name="company_index")]

    def __str__(self):
        return f"{self.name} ({self.location or 'No location'})"

    def clean(self):
        if self.location == "":
            self.location = None


class JobAdvertisement(models.Model):
    link = models.URLField("link", max_length=500, unique=True, blank=False)

    job_title = models.CharField("job title", max_length=255, blank=False)

    date_scraped = models.DateTimeField("date scraped", auto_now_add=True)

    direct_apply = models.BooleanField("direct apply", default=False)

    employment_type = models.ManyToManyField(
        EmploymentType, verbose_name="employment type", blank=True
    )

    location = models.ManyToManyField(Location, verbose_name="location", blank=True)

    home_office = models.BooleanField("home office", default=False)

    company = models.ForeignKey(
        Company, verbose_name="company", on_delete=models.CASCADE, blank=True, null=True
    )

    job_description = models.TextField("job description", blank=True, null=True)

    qualification = models.ManyToManyField(
        Qualification, verbose_name="qualification", blank=True
    )

    class Meta:
        verbose_name = "Job Advertisement"
        verbose_name_plural = "Job Advertisements"
        ordering = ["-date_scraped"]
        indexes = [
            models.Index(fields=["link"], name="job_link_index"),
            models.Index(fields=["job_title"], name="job_title_index"),
        ]

    def __str__(self):
        return f"{self.job_title} - {self.company}"
