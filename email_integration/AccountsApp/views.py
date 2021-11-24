from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def loginview(request):
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pw')
        print(f'usename entered - {u}, password entered={p}')
        user = authenticate(username=u,password=p)   #1.valid ---> user obj
                                                     #2.Invalid --->None
        print(user)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
    template_name = 'AccountsApp/login.html'
    context = {}
    return render(request,template_name,context)

def logoutview(request):
    logout(request)
    return redirect('login')

def registerview(request):
    form = RegisterForm() #blank form

    if request.method == 'POST':
        form = RegisterForm(request.POST) #filled form
        if form.is_valid():
            form.save()
            user_email = form.cleaned_data['email']
            subject = 'Email Integration Task'
            message = 'you are successfully signed in'
            recepient = user_email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recepient], fail_silently=False)

            return redirect('login')
    template_name='AccountsApp/register.html'
    context = {'form':form}
    return render(request,template_name,context)




