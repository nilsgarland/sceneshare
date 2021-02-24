import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import utc
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegisterForm
from .models import *
from .utils import get_video_id

def index(request):
    scenes = Scene.objects.order_by('-published')[:15]
    if request.user.is_authenticated:
        likes = Liker.objects.filter(user=request.user)
    else:
        likes = None
    context = {'scenes': scenes, 'likes': likes}
    return render(request, 'pages/index.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'pages/register.html', context)


def upload(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user.id
            url = request.POST['url']
            text = request.POST['text']
            date = datetime.datetime.utcnow().replace(tzinfo=utc)
            if url:
                video_id = get_video_id(url)
                if video_id == "none":
                    context = {'error': 'invalid-url'}
                    return render(request, 'pages/upload.html', context)
                else:
                    scene = Scene()
                    scene.user_id = user
                    scene.url = video_id
                    scene.text = text
                    scene.published = date
                    scene.save()
                    return HttpResponseRedirect(reverse('index'))
            else:
                context = {'error': 'empty-field'}
                return render(request, 'pages/upload.html', context)

        else:
            return render(request, 'pages/upload.html')
    else:
        return redirect('/login')


def like(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.user.id
            scene_id = int(request.POST['scene'])
            if scene_id:
                scene = get_object_or_404(Scene, pk=scene_id)
                try:
                    has_liked = scene.liker_set.get(user=user_id)
                except:
                    has_liked = None
                if has_liked:
                    like = has_liked
                    like.delete()
                else:
                    liker = Liker()
                    liker.scene = scene
                    liker.user = request.user
                    liker.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redurect('/login')


def scene(request, scene_id):
    scene = get_object_or_404(Scene, pk=scene_id)
    if request.user.is_authenticated:
        has_liked = scene.liker_set.filter(user=request.user)
        if has_liked:
            liked = True
        else:
            liked = False
    else:
        liked = False
    context = {'scene': scene, 'liked': liked}
    return render(request, 'pages/scene.html', context)


def delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            scene_id = request.POST['scene']
            scene = get_object_or_404(Scene, pk=scene_id)
            if scene.user == request.user:
                scene.delete()
                return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')