from django.shortcuts import render,get_object_or_404,redirect
from .forms import UserCreationForm,newManuscriptForm,NewComment,UserUpdateForm,ProfileUpdateForm,PDFUpdateForm
from django.contrib import messages
from .models import newManuscript,Comment,Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request,'تم الاضافة بنجاح')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'title':'Register',
        'form':form,
    }
    return render(request,'user/register.html',context)
@login_required(login_url='login')
def profile(request):
    posts = newManuscript.objects.filter(author=request.user)
    context = {
        'title': request.user,
        'user': request.user,
        'posts': posts
    }
    return render(request, 'user/profile.html', context)
@login_required(login_url='login')
def AddNewManuscript(request,user_id):
    user = User.objects.get(username=request.user)
    categorys = Category.objects.all()
    form = newManuscriptForm()
    posts = newManuscript.objects.all()
    model = newManuscript()
    new_comment = None
    if request.method=='POST':
        form = newManuscriptForm(request.POST,request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = user
            new_comment.save()
            redirect('home')
    else:
        form = newManuscriptForm()
    context = {
        'title':'Add New Manuscript',
        'form':form,
        'categorys':categorys
    }
    return render(request,'user/new_manuscripts.html',context)
@login_required(login_url='login')
def MyManuscript(request,user_id):
    Manuscripts = newManuscript.objects.filter(author=request.user)
    context = {'title':'My Manuscript',
               'Manuscripts':Manuscripts}
    return render(request,'user/my_manuscripts.html',context)
@login_required(login_url='login')
def post_detail(request,post_id):
    post = get_object_or_404(newManuscript,pk=post_id)
    comments = post.comments.filter(active=True)
    comment_form = NewComment()
    AddNewComment = Comment()
    new_comment = None
    context = {
        'title': "{} details ".format(post.title),
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            user = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = user
            new_comment.save()
            return redirect('detail', post_id)
    else:
        comment_form = NewComment()

    return render(request, 'user/detail.html', context)
@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Profile Updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title':'Update profile',
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request,'user/profile_update.html',context)
@login_required(login_url='login')
def update_manuscript(request,post_id):
    manuscript = newManuscript.objects.get(pk=post_id)
    if request.method == 'POST':
        PDF_form = PDFUpdateForm(request.POST,request.FILES,instance=manuscript)
        if PDF_form.is_valid:
            PDF_form.save()
            messages.success(
                request, 'Saved')
            return redirect('profile')
    else:
        PDF_form = PDFUpdateForm(instance=manuscript)
    context = {
        'title':'Update profile',
        'PDF_form':PDF_form,
    }
    return render(request,'user/manuscript_update.html',context)