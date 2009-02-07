# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

import settings
from models import UserProfile
from forms import LoginForm, RegistrationForm, UserProfileForm, UserForm

def user_login(request, template="userprofile/login.html"):
    info = None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(request.GET.get("next") or "/")
        info = "Zły login i/lub hasło"
    f = LoginForm()
    return render_to_response(template, {
        "form": f,
        "info": info,
        })

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/")


def register(request, template="userprofile/registration.html"):
    if request.POST:
        f = RegistrationForm(request.POST)
        if f.is_valid():
            user = User.objects.create_user(
                    f.data['username'], f.data['mail'],
                    f.data['password_pass0'])
            # this group should have been created with yaml datafile
            g = Group.objects.get(name="SimpleUser")
            user.groups.add(g)
            u = user.save()
            up = UserProfile(user=user)
            up.save()
            return HttpResponseRedirect(
                    settings.FORUM_AFTER_REGISTRATION_REDIRECT_URL)
    else:
        f = RegistrationForm()
    return render_to_response(template, {
        "form": f,
        })


@login_required
def userinfo(request, username, template="userprofile/userinfo.html"):
    user = get_object_or_404(User, username=username)
    return render_to_response(template, {
        "user": user,
        }, context_instance=RequestContext(request))

@login_required
def user_preferences(request, template="userprofile/preferences.html"):
    user = request.user
    profile = UserProfile.objects.get_or_create(user=user, defaults={})[0]
    if request.POST:
        profile_form = UserProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            # TODO
            user_form = user_form.save()
            profile_form = profile_form.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    return render_to_response(template, {
        "user_form": user_form,
        "profile_form": profile_form,
        }, context_instance=RequestContext(request))
