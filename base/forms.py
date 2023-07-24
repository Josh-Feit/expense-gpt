from django import forms

from .models import *

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['title', 'description', 'quantity', 'action_type']

class GPTEntryForm(forms.Form):

    input = forms.CharField(required=True, label='')

    class Meta:
        fields = ('input')