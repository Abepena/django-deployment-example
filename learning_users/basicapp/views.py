from django.shortcuts import render
from basicapp.forms import UserProfileInfoForm, UserForm
from . import forms

#Login imports
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'basicapp/index.html')

@login_required #requires the user to be logged in to log them out
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in,  Nice!")

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data = request.POST)
        profile_form = forms.UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password) # Sets the password as a Hash byb going into settings.py
            user.save() #Saved the hashed password to the database

            profile = profile_form.save(commit=False) #dont want to commit to the database yet otherwise may encounter collisions where the user will be overwritten
            profile.user = user # SETS UP ONE TO ONE RELATIONSHIP

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request, 'basicapp/registration.html',
                {'user_form':user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username') # gets username from login.html form
        password = request.POST.get('password') # gets password from login.html

        user = authenticate(username = username, password = password)

        if user: #if we have a user
            if user.is_active:
                login(request, user) #passes in the request, and the user that was just authenticated and logs that user in
                return HttpResponseRedirect(reverse('index')) #Redirects a successful logged in user to the view named index

            else:
                return HttpResponse("<h1>Account not Active</h1>")

        else:
            print("Someone Tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("<h1>Invalid Login details supplied</h1>")
    else:
        return render(request, 'basicapp/login.html', {})
