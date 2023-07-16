from django import forms

from art_gallery.art.models import Art, Request_Art


class BookForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = '__all__'


class RequestBookForm(forms.ModelForm):
    class Meta:
        model = Request_Art
        fields = ('art_name', 'artist')
