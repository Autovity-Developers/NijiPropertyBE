from nijiapp.models import ClientUser
from django import forms

class ClientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = ClientUser