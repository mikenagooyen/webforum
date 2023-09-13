from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Thread, Section, Comment
from .forms import ThreadForm, CommentForm

# Create your views here.

threads = [
    {'id':1, 'name':'Python Learning'},
    {'id':2, 'name':'HTML For Beginners'},
    {'id':3, 'name':'Frontend Help'},

]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)

    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form' : form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    threads = Thread.objects.filter(
        Q(section__name__icontains=q) |
        Q(name__icontains=q) |
        Q(post__icontains=q)
        )

    sections = Section.objects.all() 
    thread_count = threads.count()
    thread_comments = Comment.objects.filter(Q(thread__section__name__icontains=q))

    context = {'threads': threads, 'sections': sections,
            'thread_count': thread_count, 'thread_comments': thread_comments}
    return render(request, 'base/home.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    threads = user.thread_set.all()
    thread_comments = user.comment_set.all()
    sections = Section.objects.all()

    context = {'user': user, 'threads': threads, 
            'thread_comments': thread_comments, 'sections': sections}
    return render(request, 'base/profile.html', context)


def thread(request, pk):
    thread = Thread.objects.get(id=pk)
    thread_comments = thread.comment_set.all()
    participants = thread.participants.all()

    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            thread = thread,
            post = request.POST.get('body')
        )
        thread.participants.add(request.user)
        return redirect('thread', pk=thread.id)

    context = {'thread' : thread, 'comments': thread_comments, 'participants': participants}
    return render(request, 'base/thread.html', context)


@login_required(login_url='/login/')
def createThread(request):
    form = ThreadForm()
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/thread_form.html', context)


@login_required(login_url='/login/')
def updateThread(request, pk):
    thread = Thread.objects.get(id=pk)
    form = ThreadForm(instance=thread)

    if request.user != thread.host:
        return HttpResponse("User cannot perform this operation.")

    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/thread_form.html', context)


@login_required(login_url='/login/')
def deleteThread(request, pk):
    thread = Thread.objects.get(id=pk)

    if request.user != Thread.host:
        return HttpResponse("User cannot perform this operation.")

    if request.method == "POST":
        thread.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': thread})


@login_required(login_url='/login/')
def updateComment(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)

    if request.user != comment.user:
        return HttpResponse("User cannot perform this operation.")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/thread_form.html', context)


@login_required(login_url='/login/')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse("User cannot perform this operation.")
    
    if request.method == "POST":
        comment.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': comment})