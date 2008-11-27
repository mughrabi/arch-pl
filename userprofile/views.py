# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
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
            user.save()
            return HttpResponseRedirect(request.GET.get("next") or "/")
    else:
        f = RegistrationForm()
    return render_to_response(template, {
        "form": f,
        })


@login_required
def userinfo(request, username, template="userprofile/userinfo.html"):
    user = get_object_or_404(User, name=username)
    return render_to_response(template, {
        }, context_instance=RequestContext(request))

@login_required
def preferences(request, template="userprofile/preferences.html"):
    pass
