from django import forms

class FacebookStoryForm(forms.Form):
    url = forms.URLField(label='Facebook Story URL')
