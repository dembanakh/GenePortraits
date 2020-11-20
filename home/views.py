from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader


def home(request):
    return HttpResponse(loader.get_template('home/index.html').render({}, request))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return HttpResponse(loader.get_template('home/signup.html').render({'form': form}, request))
