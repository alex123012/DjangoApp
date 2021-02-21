from django import forms


class ExelForm(forms.Form):
    x_coord = forms.CharField(max_length=128, label='X coordinates', required=False)
    y_coord = forms.CharField(max_length=128, label='Y coordinates', required=False)


class FileForm(forms.Form):
    file = forms.FileField(label='Upload file', required=False)
