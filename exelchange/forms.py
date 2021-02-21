from django import forms


class ExelForm(forms.Form):
    x_coord = forms.CharField(max_length=128, label='X coordinates')
    y_coord = forms.CharField(max_length=128, label='Y coordinates')


# class FileForm(forms.Form):
#     file = forms.FileField(label='Upload file', required=False)
