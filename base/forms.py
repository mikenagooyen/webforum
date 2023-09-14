from django.forms import ModelForm
from .models import Thread, Comment

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'
        exclude = ['host', 'participants']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'