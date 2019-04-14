from django import forms
from hole.models import Reset


class ResetForm(forms.ModelForm):

    class Meta:
        reset = Reset
        fields = ('area', 'equip', 'data', 'time', 'new_status', 'comment')
