# -*- coding: utf-8 -*-

import time

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Login"), max_length=30)
    password = forms.CharField(label=_("Password"), max_length=30,
            widget=forms.PasswordInput())


class DualPasswordWidget(forms.Widget):
    pass0_field = '%s_pass0'
    pass1_field = '%s_pass1'

    def __init__(self, *args, **kwargs):
        super(DualPasswordWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, *args, **kwargs):
        return  "<br />".join((
                forms.PasswordInput().render(self.pass0_field % name, None),
                forms.PasswordInput().render(self.pass1_field % name, None)))

    def value_from_datadict(self, data, files, name):
        pass0 = data.get(self.pass0_field % name, None)
        pass1 = data.get(self.pass1_field % name, None)
        if pass0 and pass1:
            return (pass0, pass1)
        return None

class DualPasswordField(forms.Field):
    """
    Field used to prevent password typos by asking the same password twice
    and checking if it's the same
    """
    widget = DualPasswordWidget()
    def __init__(self, *args, **kwargs):
        super(DualPasswordField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(DualPasswordField, self).clean(value)
        if value:
            pass0, pass1 = value
            if pass0 == pass1:
                if len(pass0) < 5:
                    raise forms.ValidationError(_("Password is too short"))
                elif len(pass0) > 24:
                    raise forms.ValidationError(_("Password is too long"))
                return pass0
            raise forms.ValidationError(_('Password Missmatch.'))


class RegistrationForm(forms.Form):
    username = forms.CharField(label=_("Login"), max_length=30)
    password = DualPasswordField(label=_("Password"))
    mail = forms.EmailField(label=_("Email"))
    botprotect1 = forms.CharField(label="Jak ma na imię Alan Cox?")
    botprotect2 = forms.IntegerField(label="Który będziemy mieli rok za dwa lata?")

    def clean_username(self):
        u = self.cleaned_data['username']
        try:
            User.objects.get(username__exact=u)
            raise forms.ValidationError(_("That nick is allready in usage"))
        except User.DoesNotExist:
            return u

    def clean_botprotect1(self):
        if self.cleaned_data['botprotect1'] == "Alan":
            return True
        raise forms.ValidationError(_("poo"))

    def clean_botprotect2(self):
        if self.cleaned_data['botprotect2'] == time.gmtime().tm_year + 2:
            return True
        raise forms.ValidationError(_("poo"))


class UserProfileForm(ModelForm):
    class Meta:
        model  = UserProfile
        exclude = ('user', )

