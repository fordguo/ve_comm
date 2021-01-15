from django import forms
from django.conf import settings
from import_export.forms import ImportForm
from post_office.models import EmailTemplate


class BatchEmailForm(ImportForm):
    template = forms.ModelChoiceField(queryset=EmailTemplate.objects.all())
    sender = forms.CharField(
        widget=forms.TextInput(attrs={'size': '50'}),
        initial=settings.DEFAULT_FROM_EMAIL)
    field_order = ['template', 'import_file', 'input_format']
