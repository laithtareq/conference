from django.shortcuts import render
from user import models
# Create your views here.
def home(request):
    posts = models.newManuscript.objects.all()
    context = {
        'title': 'Home',
        'user': request.user,
        'posts': posts
    }
    return render(request,'eighthConference/home.html',context)