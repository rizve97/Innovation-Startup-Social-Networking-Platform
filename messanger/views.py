from django.shortcuts import render

from .models import Message

from django.contrib.auth.models import User

# Create your views here.

def message(request, username):

	if request.method=="POST":
		rec = request.POST.get('receiver', '')
		reci = User.objects.get(username=rec)
		msg = request.POST.get('message', '')
		picture = request.FILES.get("image", "")
		msg_obj = Message(sender=request.user, reciver=reci, msg=msg, pict=picture)
		msg_obj.save()
		print('success')

	recmsg = Message.objects.filter(reciver=request.user).order_by('-dat')
	senmsg = Message.objects.filter(sender=request.user).order_by('-dat')

	context = {
		'user' : username,
		'recmsg' : recmsg,
		'senmsg' : senmsg,
	}
	return render(request, "message/semessage.html", context)
