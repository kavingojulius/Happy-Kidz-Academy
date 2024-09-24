from django.shortcuts import render

# Create your views here.
def homepage(request):

    return render(request, 'main/index.html')

def about_us(request):

    return render(request, 'main/about_us.html')

def visionmission(request):

    return render(request, 'main/vision_mission.html')

def news(request):

    return render(request, 'main/news.html')

def notices(request):

    return render(request, 'main/notices.html')

def contact_us(request):

    return render(request, 'main/contact_us.html')

def downloads(request):

    return render(request, 'main/downloads.html')

def gallery(request):

    return render(request, 'main/gallery.html')
