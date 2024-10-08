from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from .models import Message
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

@login_required
def portal(request):
    admin_user = User.objects.get(is_superuser=True)  # Assuming admin is the superuser
    messages = Message.objects.filter(sender=request.user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=request.user)
    messages = messages.order_by('timestamp')

    # Get unread messages count
    unread_count = Message.objects.filter(receiver=request.user,sender=request.user, read=False).count()
    
    # Mark unread messages as read when the admin opens the chat
    Message.objects.filter(sender=request.user, receiver=request.user, read=False).update(read=True)

    if request.method == 'POST':
        message_text = request.POST['message']
        if message_text:
            Message.objects.create(sender=request.user, receiver=admin_user, message=message_text)
            return redirect('portal')  # Reload the page after submitting

    return render(request, 'portal/portal.html', {
        'messages': messages,
        'unread_count': unread_count,  # Pass unread count to the template
    })

@login_required
def delete_chats(request):
    if request.method == 'POST':
        admin_user = User.objects.get(is_superuser=True)
        # Delete all messages between the user and the admin
        Message.objects.filter(sender=request.user, receiver=admin_user).delete()
        Message.objects.filter(sender=admin_user, receiver=request.user).delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=403)

# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('fname')
#         last_name = request.POST.get('lname')
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password')
#         pass2 = request.POST.get('password1')

#         if pass1!=pass2:
#             return render(request, 'portal/register.html', {'error': 'Passwords dont match'})
#         else:
#             my_user=User.objects.create_user(username=uname, email=email, password=pass1, first_name=first_name, last_name=last_name)
#             my_user.save()
#             return redirect('log_in')
#     return render(request, 'portal/register.html')

def log_in(request):        
    if request.method == 'POST':        
        # email=request.POST.get('email')
        username=request.POST.get('username')
        pass1=request.POST.get('password1')
    
        # try :
        #     user_obj = User.objects.get(email=email)            
        #     user=authenticate(request, username=user_obj.username, password=pass1)
        # except User.DoesNotExist:
        #     user = None

        user=authenticate(request, username=username, password=pass1)

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
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('portal')  # Redirect back to the portal after success
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'portal/change_password.html', {'form': form})

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to keep the user logged in
#             messages.success(request, 'Your password has been changed successfully.')
#             return JsonResponse({'message': 'Your password has been changed successfully.'})
#         else:
#             return JsonResponse({'message': 'Error changing password.'}, status=400)
    
#     form = PasswordChangeForm(request.user)
#     return render(request, 'portal/change_password.html', {'form': form})


@login_required
def admin_conversations(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Get users who have sent messages to the admin
    users = User.objects.filter(sent_messages__receiver=request.user).distinct()

    users_with_unread = {}
    for user in users:
        unread_count = Message.objects.filter(sender=user, receiver=request.user, read=False).count()
        users_with_unread[user.id] = unread_count

    # If it's an AJAX request, return the list of users and their unread counts
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'users': list(users.values()),
            'users_with_unread': users_with_unread
        })

    return render(request, 'portal/admin_conversations.html', {
        'users': users,
        'users_with_unread': users_with_unread,
    })


@csrf_exempt
@login_required
def delete_conversation(request):
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        # Assuming Message is the model for chat messages
        Message.objects.filter(sender=user, receiver=request.user).delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=403)


def check_new_users(request):
    """Function to check for new users who have sent messages."""
    if request.user.is_superuser:
        new_users = User.objects.filter(sent_messages__receiver=request.user).exclude(id__in=users)
        new_users_list = [{'id': user.id, 'username': user.username} for user in new_users]
        return JsonResponse({'new_users': new_users_list})
    return JsonResponse({'new_users': []})


@login_required
def admin_chat(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')  # Restrict access to admin

    user = User.objects.get(id=user_id)
    admin_user = request.user

    # Fetch all messages between the admin and the user
    messages = Message.objects.filter(sender=user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=user)
    messages = messages.order_by('timestamp')

    # Mark unread messages as read when the admin opens the chat
    Message.objects.filter(sender=user, receiver=admin_user, read=False).update(read=True)

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

    # Mark all unread messages from admin as read when user opens the chat
    if not request.user.is_superuser:
        Message.objects.filter(sender=admin_user, receiver=user, read=False).update(read=True)

    # Convert the queryset to JSON
    messages_json = serializers.serialize('json', messages)
    return JsonResponse({'messages': messages_json})


