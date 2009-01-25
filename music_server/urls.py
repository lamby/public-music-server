from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('music_server.media.views',
    url(r'^$', 'index', name='index'),
    url(r'^youtube', 'youtube', name='youtube'),
    url(r'^xhr/queue', 'xhr_queue', name='xhr-queue'),
    url(r'^a/item/delete/(?P<item_id>\d+)$', 'delete', name='delete-item'),
    url(r'^a/item/(?P<direction>(up|down))/(?P<item_id>\d+)$', 'move', name='move-item'),
)

urlpatterns += patterns('music_server.profile.views',
    url(r'^begin', 'setup_profile', name='setup-profile'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': './site_media/', 'show_indexes': True},
            name='site-media'),
    )
