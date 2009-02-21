from django.forms import ModelForm

from models import MessageBox


class MessageBoxForm(ModelForm):
    class Meta:
        model = MessageBox
        fields = ("receiver", "text")

