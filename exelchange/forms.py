from django import forms


class ExelForm(forms.Form):
    x_coord = forms.TimeField(label='X coordinates')
    y_coord = forms.TimeField(label='Y coordinates')