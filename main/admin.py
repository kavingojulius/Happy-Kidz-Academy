from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(DownloadMaterials)
class DownloadMaterialsAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

admin.site.register(Gallery)