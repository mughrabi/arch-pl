# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from models import Thread, Post


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ('title', )

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', )


class AdvancedSearchForm(forms.Form):
    searchtext = forms.CharField(label="Szukana fraza",
            min_length=4, max_length=100, required=False)
    user = forms.CharField(label="Nazwa użytkownika", required=False)
    solved = forms.BooleanField(
            label="Tylko tematy oznaczone jako rozwiązane", required=False)
    closed = forms.BooleanField(label="Tylko zamknięte tematy", required=False)

    # TODO - walidacja
