from django.contrib import admin

# Register your models here.
 
from .models import Section, Thread, Comment

admin.site.register(Section)
admin.site.register(Thread)
admin.site.register(Comment)