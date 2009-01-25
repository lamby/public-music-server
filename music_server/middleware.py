from django.utils.functional import memoize
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from music_server.profile.models import Profile

ARP_CACHE = {}

def ip_to_mac(ip):
    # Actually look up MAC address
    # Use django.core.cache instead of memoize
    return ip
ip_to_mac = memoize(ip_to_mac, ARP_CACHE, 1)

class MACAuthenticationMiddleware(object):
    WHITELIST = (
        reverse('site-media', args=('',)),
        reverse('setup-profile', args=()),
    )

    def process_request(self, request):
        mac = ip_to_mac(request.META.get('REMOTE_ADDR'))

        try:
            request.user = User.objects.get(username=mac)
        except:
            request.user = User.objects.create(
                username=mac,
            )
            Profile.objects.create(
                user=request.user,
            )

        if not request.user.profile.nickname:
            for url in self.WHITELIST:
                if request.path.startswith(url):
                    return

            return HttpResponseRedirect(reverse('setup-profile'))
