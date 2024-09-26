from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def portal(request):

    return render(request, 'portal/portal.html')

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
