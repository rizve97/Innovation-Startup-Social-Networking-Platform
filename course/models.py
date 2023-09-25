from django.db import models
from django.contrib.auth.models import User

class coursePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to = "CoursePost", blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return str(self.user) + ' '+ str(self.date.date())

class coursePage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    userImage = models.ImageField(upload_to = "Profiles")
    conductedcourse = models.IntegerField(default=0)
    enrolledcourse = models.IntegerField(default=0)

    def _str_(self):
        return str(self.user)


class Enroll(models.Model):
    user = models.ManyToManyField(User, related_name="enrollinguser")
    course = models.OneToOneField(coursePost, on_delete=models.CASCADE)

    @classmethod
    def enroll(cls, course, enrolling_user):
        obj, create = cls.objects.get_or_create(course = course)
        obj.user.add(enrolling_user)

    @classmethod
    def dismiss(cls, course, dismissing_user):
        obj, create = cls.objects.get_or_create(course = course)
        obj.user.add(dismissing_user)

    def _str_(self):
        return str(self.course)
