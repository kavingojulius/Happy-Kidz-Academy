from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

@login_required
def portal(request):
    admin_user = User.objects.get(is_superuser=True)  # Assuming admin is the superuser
    messages = Message.objects.filter(sender=request.user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        message_text = request.POST['message']
        if message_text:
            Message.objects.create(sender=request.user, receiver=admin_user, message=message_text)
            return redirect('portal')  # Reload the page after submitting

    return render(request, 'portal/portal.html',  {'messages': messages})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')

        if pass1!=pass2:
            return render(request, 'portal/register.html', {'error': 'Passwords dont match'})
        else:
            my_user=User.objects.create_user(username=uname, email=email, password=pass1, first_name=first_name, last_name=last_name)
            my_user.save()
            return redirect('log_in')
    return render(request, 'portal/register.html')


def log_in(request):        
    if request.method == 'POST':        
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        
        try :
            user_obj = User.objects.get(email=email)            
            user=authenticate(request, username=user_obj.username, password=pass1)
        except User.DoesNotExist:
            user = None
            
        if user is not None:
            login(request,user)
            return redirect('portal')
        else:
            return redirect('log_in')
        
    return render(request, 'portal/log_in.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def admin_conversations(request):
    if not request.user.is_superuser:
        return redirect('home')  # Restrict access to admin

    # Get distinct users who have sent messages
    users = User.objects.filter(sent_messages__receiver=request.user).distinct()

    return render(request, 'portal/admin_conversations.html', {'users': users})

@login_required
def admin_chat(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')  # Restrict access to admin

    user = User.objects.get(id=user_id)
    admin_user = request.user
    messages = Message.objects.filter(sender=user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        message_text = request.POST['message']
        if message_text:
            Message.objects.create(sender=admin_user, receiver=user, message=message_text)
            return redirect('admin_chat', user_id=user.id)

    return render(request, 'portal/admin_chat.html', {'messages': messages, 'user': user})

@login_required
def get_messages(request, user_id=None):
    admin_user = request.user if request.user.is_superuser else User.objects.get(is_superuser=True)
    user = User.objects.get(id=user_id) if user_id else request.user

    messages = Message.objects.filter(sender=user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=user)
    messages = messages.order_by('timestamp')

    # Convert the queryset to JSON
    messages_json = serializers.serialize('json', messages)
    return JsonResponse({'messages': messages_json})


