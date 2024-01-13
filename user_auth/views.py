from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
import json

def login_view(request):
    if request.method == 'POST':
        print(f'request post:{request}')
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        user = auth.authenticate(username=username, password=password)
        print(f'user::{user}')
        if user is not None:
            auth.login(request, user)
            return JsonResponse(status=200, data={'username':user.username})
        else:
            messages.info(request, "Invailid Credential")
            return JsonResponse(status=402, data={'message':'Invailid Credential'})
    # else:
    #     print(f'request get:{request}')
    #     print(f'request get:{request.method}')
    #     return render(request, template_name='user_auth/login.html', context={})
    
def register_view(request):
    if request.method == 'POST':
        print(f'request post:{request}')
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        confirm_password = data['confirmPassword']
        email = data['email']
        user_obj = User.objects.filter(email=email)
        if user_obj:
            return JsonResponse(status=400, data={'message':'You have already registered with this email'})
        user_obj = User.objects.filter(username=username)
        if user_obj:
            return JsonResponse(status=400, data={'message':'User already exist, please try with another username'})
        if password != confirm_password:
            return JsonResponse(status=400, data={'message':'Password and confirm password does not match'})
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        print(f'user::{user}')
        return JsonResponse(status=200, data={'username':user.username})
    # else:
    #     print(f'request get:{request}')
    #     print(f'request get:{request.method}')
    #     return render(request, template_name='user_auth/register.html', context={})