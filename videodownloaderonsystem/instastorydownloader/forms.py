from django import forms

class InstagramStoryForm(forms.Form):
    url = forms.URLField(label='Instagram Story URL')
