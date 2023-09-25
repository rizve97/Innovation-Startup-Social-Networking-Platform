from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def  home(request) :
    return render(request, 'account/signup.html')

def signup(request) :

    context = {
        'finame' : '',
        'laname' : '',
        'uname' : '',
        'mail' : '',
        'pas' : '',
        'apas' : '',
    }

    if request.method == 'POST' :
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confpassword = request.POST.get('confpassword', '')

        userCheck = User.objects.filter(username=username) | User.objects.filter(email=email)

        if userCheck:
            messages.error(request, "already taken")
            return redirect('/')

        if password == confpassword and password != '':
            user = User.objects.create_user(first_name = firstname, last_name = lastname, password = password, email = email, username = username)
            user.save()
            return render(request, 'account/signup.html', context)
        else :
            messages.error(request, "Recheck your credentials.")
            context['finame'] = firstname
            context['laname'] = lastname
            context['uname'] = username
            context['mail'] = email
            context['pas'] = password
            context['apas'] = confpassword
            return render(request, 'account/signup.html', context)

    else :
        return render(request, 'account/signup.html', context)

def userLogin(request) :
    if request.method == "POST" :
        userName = request.POST.get('username', '')
        userPassword = request.POST.get('password', '')

        # if user account is exist or not
        user = authenticate(username = userName, password = userPassword)

        if user is not None :
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('/userpage')
        else :
            messages.error(request, 'Invalid Credentials')
            return redirect('/')

def userLogout(request) :
    logout(request)
    messages.success(request, 'Logged Out')
    return redirect('/')

class Change_Password(TemplateView):
    template_name = "account/password_change.html"

    def post(self, request):
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user = request.user)
            messages.success(request, "Password Changed Successfully")
            return redirect("/")
        else:
            for err in form.errors.values():
                messages.error(request, err)
            return redirect("/change_password")

    def get(self, request):
        form = PasswordChangeForm(user = request.user)
        return render(request, self.template_name, {"form":form})


    #/*p ; {  * P " : _ [*/
