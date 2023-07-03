from django.forms import ModelForm
from .models import Thread

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'