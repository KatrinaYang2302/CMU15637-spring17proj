from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from project.models import *
from project.forms import *

from twilio.rest import TwilioRestClient
from random import randint
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponse, Http404

from social_django.models import UserSocialAuth

ACCOUNT_SID = "ACc5a25e13fbe3cdb8bb07aaa43dc2735b";
AUTH_TOKEN = "5ce3fd2eb3b66865e100dc04c23decf8";
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN);

# Create your views here.

def cover(request):
	context = {}
    #context['fav_rt'] = fav_rt.objects.get(user = request.user)

	if request.user.is_authenticated():
		context['loggedin'] = 1

	return render(request, 'project/cover.html', context)

def home(request):
    context = {}

    if request.user.is_authenticated():
        context['loggedin'] = 1

    return render(request, 'project/home.html', context)

@login_required
def logout(request):
    context = {}
    context['loggedin'] = 0
    return render(request, 'project/cover.html', context)

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'project/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'project/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username = form.cleaned_data['username'],
										password = form.cleaned_data['password1']) 
    									
    new_user.save()
    new_user_profile = bus_user(user=new_user)
    new_user_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))
 
def sendRouteText(request):
    client.messages.create(
    to="14123209785", 
    from_="14125672801 ", 
    body=request.POST['routeresult'], 
    )
    return redirect(reverse('home'));

@login_required
@transaction.atomic
def edit_overview(request):
    context = {}
    context['form'] = ProfilePswForm()
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    context['github_login'] = github_login
    context['google_login'] = google_login
    context['email'] = user.email
    context['can_disconnect'] = can_disconnect
	
    return render(request, 'project/edit-profile.html', context)


@login_required
@transaction.atomic
def edit_name(request):
    context = {}
    user = request.user

    user_profile = bus_user.objects.get(user = user)
    if request.method == 'GET':
        edit_overview(request)

    user.username = request.POST['username']
    user.email = request.POST['email']
    user.save()

    form = ProfilePswForm()
    context['form'] = form
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    context['github_login'] = github_login
    context['google_login'] = google_login
    context['email'] = user.email
    context['can_disconnect'] = can_disconnect
    return render(request, 'project/edit-profile.html', context)

@login_required
@transaction.atomic
def change_password(request):
    context = {}
    errors = []
    form = ProfilePswForm()
    context['form'] = form
    if request.method == "POST":
        form = ProfilePswForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = form.cleaned_data['old_password']
            newpassword1 = form.cleaned_data['password1']
            newpassword2 = form.cleaned_data['password2']
            user = authenticate(username = username, password = oldpassword)
            if user:
                if newpassword1 == newpassword2:
                    user.set_password(newpassword1)
                    user.save()
                    context['message'] = "New password saved."
                    user = authenticate(username=user.username,
                                        password=newpassword1)
                    login(request, user)
                    return render(request, 'project/edit-profile.html', context)
                else:
                    errors.append("New passwords are different.")
                    context['errors'] = errors
                    return render(request, 'project/edit-profile.html', context)
            else:
                errors.append("Old password is incorrect.")
                context['errors'] = errors
                return render(request, 'project/edit-profile.html', context)
        
        errors.append("Invalid.")
        context['errors'] = errors
        user = request.user

        try:
            github_login = user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None
        try:
            google_login = user.social_auth.get(provider='google-oauth2')
        except UserSocialAuth.DoesNotExist:
            google_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
        context['github_login'] = github_login
        context['google_login'] = google_login
        context['email'] = user.email
        context['can_disconnect'] = can_disconnect
        return render(request, 'project/edit-profile.html', context)

@login_required
def sendVerifyCode(request, phoneNum):
    verifycode=""
    count = 0
    while count<4:
        verifycode=verifycode+str(randint(0,9))
        count=count+1

    rst = []
    rst.append(verifycode)

    client.caller_ids.validate("+"+phoneNum, friendly_name=request.user.username)
    client.messages.create(
        to=phoneNum, 
        from_="14125672801",
        body=verifycode, 
    )

    return HttpResponse(rst, content_type = 'application/json')

@login_required
@csrf_exempt
def add_fav_lo(request):
    print(request.POST)
    address = request.POST.get('address', False)
    latitude = request.POST.get('latitude', False)
    longitude = request.POST.get('longitude', False)
    print(address)
    print(latitude)
    print(longitude)
    print("***********")

    context = {}
    context['form'] = ProfilePswForm()
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    context['github_login'] = github_login
    context['google_login'] = google_login
    context['email'] = user.email
    context['can_disconnect'] = can_disconnect
    
    return render(request, 'project/edit-profile.html', context)
