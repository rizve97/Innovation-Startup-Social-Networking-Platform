from django.contrib import admin
from course.models import coursePost, coursePage, Enroll

# Register your models here.

admin.site.register(coursePost)
admin.site.register(coursePage)
admin.site.register(Enroll)