from django.forms import ModelForm

from music_server.profile.models import Profile

class SetupForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname',)
