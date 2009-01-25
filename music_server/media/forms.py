from django.forms import forms, ModelForm

from music_server.media.models import Item, YouTubeQueue

class UploadForm(ModelForm):
    class Meta:
        model = Item
        fields = ('file',)

class YouTubeForm(ModelForm):
    class Meta:
        model = YouTubeQueue
        fields = ('uri',)
