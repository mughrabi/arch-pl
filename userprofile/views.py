# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from forms import LoginForm, RegistrationForm

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
    return render_to_response(template, {
        "form": LoginForm(),
        "info": info,
        })

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/")


def register(request, template="userprofile/registration.html"):
    if request.POST:
        pass
    form = RegistrationForm()
    return render_to_response(template, {
        "form": form,
        })


@login_required
def userinfo(request, username, template="userprofile/userinfo.html"):
    user = get_object_or_404(User, name=username)
    return render_to_response(template, {
        }, context_instance=RequestContext(request))

@login_required
def preferences(request, template="userprofile/preferences.html"):
    pass
