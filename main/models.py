from django.db import models
from django.utils import timezone

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