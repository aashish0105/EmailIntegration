from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def homeview(request):
    template_name='firstapp/home.html'
    context = {}
    return render(request, template_name, context)

@login_required(login_url='login')
def aboutusview(request):
    template_name = 'firstapp/aboutus.html'
    context = {}
    return render(request, template_name, context)