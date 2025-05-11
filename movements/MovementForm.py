from django import forms
from dbmodels.models import Movements

class MovementForm(forms.ModelForm):
    class Meta:
        model = Movements
        fields = ['variant', 'source_warehouse', 'destination_warehouse', 'quantity', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
