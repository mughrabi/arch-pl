from django.utils.translation import ugettext_lazy as _
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=_("Login"), max_length=30)
    password = forms.CharField(label=_("Password"), max_length=30,
            widget=forms.PasswordInput())


class RegistrationForm(forms.Form):
    username = forms.CharField(label=_("Login"), max_length=30)
    password = forms.CharField(label=_("Password"), max_length=30,
            widget=forms.PasswordInput())
    password_2 = forms.CharField(label=_("Password (repeat)"), max_length=30,
            widget=forms.PasswordInput())
    mail = forms.EmailField(_("email"))


