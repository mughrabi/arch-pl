from django.forms import ModelForm
from django import forms
from models import Thread, Post


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ('title', 'keywords')

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', )


class AdvancedSearchForm(forms.Form):
    search = forms.CharField(min_length=4, help_text="bla")

