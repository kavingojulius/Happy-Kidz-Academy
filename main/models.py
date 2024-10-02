from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class LandingPageText(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    

class Event(models.Model):
    title = models.CharField(max_length=255)  # Title of the event
    image = models.ImageField(upload_to='events_images')  # Image field for the event
    content = models.TextField()  # Content description of the event
    start_time = models.DateTimeField()  # Event start time
    end_time = models.DateTimeField()  # Event end time
    
    def is_event_active(self):
        """Check if the event is still active (current time is before end time)"""
        return timezone.now() < self.end_time
    
    def time_remaining(self):
        """Calculate time remaining until the event ends"""
        if self.is_event_active():
            return self.end_time - timezone.now()
        return None
    
    def __str__(self):
        return self.title


class DownloadMaterials(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='Download_Materials/') # Files will be uploaded to MEDIA_ROOT/pdfs
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Download Materials(such as PDFS,... etc)'
    

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Gallery (images)'

class StudentAdmission(models.Model):
    # Student Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    CLASS_CHOICES = [
        ('daycare', 'Daycare'),
        ('playgroup', 'Playgroup'),
        ('kindergarten', 'Kindergarten'),
        ('grade1', 'Grade 1'),
        ('grade2', 'Grade 2'),
        ('grade3', 'Grade 3'),
    ]
    applying_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    
    # Parent/Guardian Information
    parent_first_name = models.CharField(max_length=50)
    parent_last_name = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField()
    home_address = models.TextField()

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)

    # Timestamp
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applying_class}"