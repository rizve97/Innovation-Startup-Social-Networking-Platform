from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from course.models import coursePost, coursePage, Enroll
import json


def courseHome(request):
    #filter(user__in = followed_users).order_by('-pk') | Post.objects.filter(user = request.user).order_by('-pk')
    posts = coursePost.objects.all().order_by("-pk")
    enrolled = [i for i in posts if Enroll.objects.filter(course = i, user = request.user)]
    data = {
        'posts':posts,
        "enrolled_course":enrolled,
    }
    return render(request, "course/postcourse.html", data)

def post(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        image = request.FILES["image"]
        date = request.POST.get('date', '')
        user = request.user
        print(user, title, description, image, date, end='\n')
        post_obj = coursePost(title=title, description=description, image=image, date=date, user=user)
        post_obj.save()
        messages.success(request, 'Showed')
        return redirect('/course')

    else:
        messages.error(request, 'wrong')
        return redirect('/course')

def userCourse(request, username):
    user = User.objects.filter(username=username)
    if user:
        course = Course.objects.get(user=user[0])
        bio = course.bio
        conductedcourse = course.conductedcourse
        enrolledcourse = course.enrolledcourse
        data = {'user_obj':user, 'bio':bio, 'conductedcourse':conductedcourse, 'enrolledcourse':enrolledcourse}


    return redirect(request, "course/postcourse.html", data)

def delCourse(request, courseId):

    course = coursePost.objects.filter(pk=courseId)
    image_path = course[0].image.url
    course.delete()
    messages.info(request, "Post Deleted")
    return redirect('/course')

def enrollCourse(request):
    course_id = request.GET.get("enrollId", "")
    course = coursePost.objects.get(pk=course_id)
    user = request.user
    enroll = Enroll.objects.filter(course = course, user=user)
    enrolled = False

    if enroll:
        Enroll.dismiss(course, user)
    else:
        enrolled = True
        Enroll.enroll(course, user)

    resp = {
        'enrolled':enrolled
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")

