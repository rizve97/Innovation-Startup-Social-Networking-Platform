from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Profile, Like, Following, Comment
from django.conf import settings
import json
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from random import shuffle
from django.http import HttpResponseRedirect
from course.models import coursePost

def userHome(request):
    #fetching post from database
    user = Following.objects.get(user = request.user) #following_obj of user

    followed_users = user.followed.all()
    #filter(user__in = followed_users).order_by('-pk') | Post.objects.filter(user = request.user).order_by('-pk')
    postall = Post.objects.all()
    posts = list(postall)
    shuffle(posts)
    liked_ = [i for i in posts if Like.objects.filter(post = i, user = request.user)]
    comments = {}
    for p in posts :
        coma = Comment.objects.filter(post=p)
        comments[p.id] = coma
    data = {
        'posts':posts,
        "liked_post":liked_,
        "comments":comments,
    }
    return render(request, "userpage/postfeed.html", data)
    

def post(request):
    if request.method=="POST":
        image_ = request.FILES['image']
        captions_ = request.POST.get('captions','')
        user_ = request.user
        post_obj = Post(user=user_, caption=captions_, image=image_)
        post_obj.save()
        messages.success(request, "We Showed Them!!!")
        return redirect('/')
    else:
        messages.error(request, "Something went Wrong :(")
        return redirect('/')


def delPost(request, ID):
    # every post have a unique identity
    post_ = Post.objects.filter(pk=ID)
    image_path = post_[0].image.url #image location in system
    post_.delete()
    messages.info(request, "Post Deleted")
    return redirect('/userpage')


def showpost(request, ID):
    post = Post.objects.get(id=ID)
    comments = {}
    coma = Comment.objects.filter(post=post)
    comments[post.id] = coma
    context = {
        'post' : post,
        'comments' : comments,
    }
    return render(request, 'userpage/postshowing.html', context)


def userProfile(request, username):
    user = User.objects.filter(username=username)
    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        post = Post.objects.filter(user=user)
        bio = profile.bio
        conn = profile.connection
        user_img = profile.userImage
        is_following = Following.objects.filter(user = request.user, followed = user)
        #create a Following objects
        following_obj = Following.objects.get(user = user)
        follower, following = following_obj.follower.count(), following_obj.followed.count()
        liked_ = [i for i in post if Like.objects.filter(post = i, user = request.user)]
        comments = {}
        for p in post :
            coma = Comment.objects.filter(post=p)
            comments[p.id] = coma

        data = {
            'user_obj':user,
            'bio':bio,
            'conn':conn,
            'follower':follower,
            'following':following,
            'userImg':user_img,
            'posts':post,
            'connection':is_following,
            "liked_post":liked_,
            'comments':comments,
        }
    else: return HttpResponse("NO SUCH USER")

    return render(request, 'userpage/userProfile.html', data)


def getPost(user):
    post_obj = Post.objects.filter(user=user)
    imgList= [post_obj[i:i+3] for i in range(0, len(post_obj), 3)]
    return imgList


def likePost(request):
    post_id = request.GET.get("likeId", "")
    post = Post.objects.get(pk=post_id)
    user = request.user
    like = Like.objects.filter(post = post, user=user)
    liked = False

    if like:
        Like.dislike(post, user)
    else:
        liked = True
        Like.like(post, user)

    resp = {
        'liked':liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")

def comment(request):
    sender = request.user
    comment = request.POST.get('comment', '')
    postiden = request.POST.get('postid', '')
    post = Post.objects.get(id=postiden)
    commentobj = Comment(post=post, user=sender, cmnt=comment)
    commentobj.save()
    print('success')
    return redirect('/userpage')

def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username = username)

    #check if already following
    following = Following.objects.filter(user = main_user, followed = to_follow)
    is_following = True if following else False

    if is_following:
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True

    resp = {
        "following" : is_following,
    }

    response = json.dumps(resp)
    return HttpResponseRedirect('/userpage/'+ to_follow.username)
    #HttpResponse(response, content_type="application/json")

'''class Search_User(ListView):
    model = User
    template_name = "userpage/searchUser.html"
    paginate_by = 5 #page_obj

    def get_queryset(self):
        select = self.request.GET.get("search", '')
        print(select)
        username = self.request.GET.get("username", None)
        queryset = User.objects.filter(username__icontains = username).order_by('-id')
        return queryset '''

def search(request):
    val = request.POST.get("searching", "")
    print(val)
    seruser = User.objects.filter(username__icontains = val).order_by('-id')
    serpost = Post.objects.filter(caption__icontains = val).order_by('-id')
    sercourse = coursePost.objects.filter(title__icontains = val).order_by('-id')
    context = {
        'searchusers' : seruser,
        'searchposts' : serpost,
        'searchcourses' : sercourse, 
    }
    return render(request, 'userpage/search.html', context)

class EditProfile(View):
    def post(self, request, *args, **kwargs):
        profile_obj = Profile.objects.get(user = request.user)
        bio = request.POST.get("Bio", "")
        img = request.FILES.get("image", "")
        if bio: profile_obj.bio = bio
        if img: profile_obj.userImage = img
        profile_obj.save()

        return HttpResponseRedirect(reverse("userpage:user_profile", args=(request.user.username,)))
