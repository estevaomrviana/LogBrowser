from django import forms

class SSHConnectionForm(forms.Form):
    hostname = forms.CharField(
        label="Hostname",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
    )
    port = forms.IntegerField(
        label="Port",
        initial=22,
        widget=forms.NumberInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
    )
    remote_directory = forms.CharField(
        label="Remote Directory",
        initial="/",
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'})
    )
