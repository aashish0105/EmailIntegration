from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import *
from django.core.mail import send_mail,BadHeaderError
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.utils.encoding import force_text
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
            login(request, user)
            subject = 'Send Email Django Task'
            message = user.username + "," + 'you are successfully logged in'
            recepient = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recepient], fail_silently=False)
            #template_name = 'accounts/success.html'
            #context = {'recepient': recepient}
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
    template_name = 'AccountsApp/login.html'
    context = {}
    return render(request,template_name,context)

def logoutview(request):
    logout(request)
    return redirect('login')

'''
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

'''

def registerview(request):
    if request.method == 'POST':
        print('In request POST')
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('In form is valid')
            email = form.cleaned_data.get('email')
            if not User.objects.filter(email__iexact=email).exists():
                print('In email iexact count 1')
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('AccountsApp/email_template.txt', {
                            'user': user,
                            'domain': '127.0.0.1:8000',
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            'protocol': 'http',
                        })
                to_email = form.cleaned_data.get('email')
                try:
                    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                messages.error(request, 'Entered Email Already Exists')
    else:
        form = RegisterForm()

    return render(request, 'AccountsApp/register.html', {'form': form})

def activate(request, uidb64, token):
    #User = get_user_model()
    global success
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('success')
    else:
        user.delete()
        return HttpResponse('Activation link is invalid!')

def email_verification_success(request):
    template_name = "AccountsApp/verification_success.html"
    context = {}
    return render(request,template_name,context)

