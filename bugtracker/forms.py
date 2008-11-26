from django.forms import ModelForm
from models import Bug, BugComment


class BugForm(ModelForm):
    class Meta:
        model = Bug
        fields = ('title', 'description')

class BugCommentForm(ModelForm):
    class Meta:
        model = BugComment
        fields = ('text')
