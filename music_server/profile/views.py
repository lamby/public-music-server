from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from music_server.profile.forms import SetupForm

def setup_profile(request):
    if request.method == 'POST':
        form = SetupForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = SetupForm()

    return render_to_response('setup.html', {
        'setup_form': form,
    }, RequestContext(request))
