from django.shortcuts import render
from .models import *

# Create your views here.
def homepage(request):
    try:
        # Get the latest event
        event = Event.objects.filter(end_time__gte=timezone.now()).order_by('start_time').first()
        time_remaining = event.time_remaining() if event else None

        
        if event:
            # Convert event end_time to a timestamp format
            event_end_timestamp = event.end_time.timestamp()
        else:
            event_end_timestamp = None        
    except Event.DoesNotExist:
        event = None
        days = hours = minutes = seconds = 0

    return render(request, 'main/index.html', {
        'event': event,
        'event': event,
        'event_end_timestamp': event_end_timestamp,  # Send the end time as a timestamp
    })
    

def about_us(request):

    return render(request, 'main/about_us.html')

def visionmission(request):

    return render(request, 'main/vision_mission.html')

def news(request):

    return render(request, 'main/news.html')

def events(request):

    return render(request, 'main/events.html')

def contact_us(request):

    return render(request, 'main/contact_us.html')

def downloads(request):
    pdfs = DownloadMaterials.objects.all()
    return render(request, 'main/downloads.html', {'pdfs': pdfs})

def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, 'main/gallery.html', {'gallery':gallery})
