from itertools import count, izip

from django.db import connection
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse

from music_server.media.forms import UploadForm, YouTubeForm
from music_server.media.models import Item, YouTubeQueue

def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            q = form.save(commit=False)
            q.user = request.user
            q.ip = request.META.get('REMOTE_ADDR')
            q.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UploadForm()

    return render_to_response('index.html', {
        'queue': izip(count(1), Item.unplayed.all()),
        'upload_form': form,
        'youtube_form': YouTubeForm(),
    }, RequestContext(request))

def xhr_queue(request):
    return render_to_response('queue.html', {
        'queue': izip(count(1), Item.unplayed.all()),
    }, RequestContext(request))

def youtube(request):
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.user = request.user
            q.ip = request.META.get('REMOTE_ADDR')
            q.save()
            return HttpResponseRedirect(reverse('youtube'))
    else:
        form = YouTubeForm()

    return render_to_response('youtube.html', {
        'youtube_form': form,
        'queue': YouTubeQueue.objects.exclude(state='f'),
        'failed': YouTubeQueue.objects.filter(state='f')[:5],
    }, RequestContext(request))

def delete(request, item_id):
    get_object_or_404(Item, id=item_id, user=request.user, state='q').delete()
    return HttpResponseRedirect(reverse('index'))

def move(request, direction, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user, state='q')
    if direction == 'up':
        val = item.move_up()
    else:
        val = item.move_down()

    if request.is_ajax():
        if val is None:
            return HttpResponse(0)
        else:
            return HttpResponse(val.id)

    return HttpResponseRedirect(reverse('index'))
