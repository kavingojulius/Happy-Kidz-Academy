from django.db import models

# Create your models here.
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