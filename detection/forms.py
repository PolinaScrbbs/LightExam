# detection/forms.py
# detection/forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept': 'image/*,video/*'}))
