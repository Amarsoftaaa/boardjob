from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CANDIDATE = "CANDIDATE", "Candidate"
        COMPANY = "COMPANY", "Company"

    role = models.CharField(max_length=10, choices=Role.choices)



class CandidateProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='candidate_profile')
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    cv = models.FileField(upload_to='cv/',null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} -> {self.first_name} -> {self.last_name}"



class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='company_profile')
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    website = models.URLField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Job(models.Model):


    CHOICE_TYP_JOB = [
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
        ("on_site", "On site"),
    ]

    EMPLOYMENT_TYPE = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    company= models.ForeignKey(Company,on_delete=models.CASCADE,related_name='jobs')
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100,choices=CHOICE_TYP_JOB)
    employment_type = models.CharField(max_length=100,choices=EMPLOYMENT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.title


class Application(models.Model):

    CHOICE_TYPE_APPLICATION = [
        ("submitted", "Submitted"),
        ("viewed", "Viewed"),
        ("rejected", "Rejected"),
    ]

    candidate = models.ForeignKey(CandidateProfile,on_delete=models.CASCADE,related_name='applications')
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=CHOICE_TYPE_APPLICATION,default='submitted')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["candidate", "job"], name="unique_candidate_job_application")
        ]

        def __str__(self):
            return f"{self.candidate.user.username} -> {self.job.title}"

class Messages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='received_messages')
    job = models.ForeignKey(Job,on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


