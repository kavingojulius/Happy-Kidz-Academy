from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
from django.utils import timezone
from .models import Event, LandingPageText

def homepage(request):
    # Get the landing page text
    landing_page_text = LandingPageText.objects.all()

    # Fetch all upcoming events (events that haven't ended yet)
    events = Event.objects.filter(end_time__gte=timezone.now()).order_by('start_time')

    # Create a list of end timestamps for all events
    event_end_timestamps = [event.end_time.timestamp() for event in events]

    return render(request, 'main/index.html', {
        'events': events,  # Pass all events here
        'event_end_timestamps': event_end_timestamps,  # List of end timestamps for JS countdown
        'landing_page_text': landing_page_text,
    })

def about_us(request):

    return render(request, 'main/about_us.html')

def visionmission(request):

    return render(request, 'main/vision_mission.html')

def news(request):
    news_items = News.objects.all().order_by('-date')

    return render(request, 'main/news.html', {'news_items': news_items})

def events(request):

    # Fetch all upcoming events
    events = Event.objects.filter(end_time__gte=timezone.now()).order_by('start_time')

    # Create a list of end timestamps for all events
    event_end_timestamps = [event.end_time.timestamp() for event in events]

    return render(request, 'main/events.html', {
        'events': events,  # Pass all events here
        'event_end_timestamps': event_end_timestamps,  # List of end timestamps for JS countdown
    })

def contact_us(request):

    return render(request, 'main/contact_us.html')

def downloads(request):
    pdfs = DownloadMaterials.objects.all()
    return render(request, 'main/downloads.html', {'pdfs': pdfs})

def gallery(request):
    gallery = Gallery.objects.all()
    return render(request, 'main/gallery.html', {'gallery':gallery})

def admission(request):
    if request.method == 'POST':
        form = StudentAdmissionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('admission_success')  # Redirect to a success page after submission
    else:
        form = StudentAdmissionForm()
    return render(request, 'main/admission.html', {'form':form})

def admission_success(request):    
    return render(request, 'main/admission_success.html')

