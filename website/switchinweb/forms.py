from django import forms
from switchinweb.models import PolicyDoc

class PolicyForm(forms.ModelForm):
    class Meta:
        model = PolicyDoc
        fields = ['city', 'mileage', 'document']

class ManualForm(forms.Form):
    company_name        = forms.CharField(label='company_name', max_length=200)
    policy_number       = forms.CharField(label='policy_number', max_length=30)
    effective_date      = forms.CharField(label='effective_date', max_length=30)
    expiration_date     = forms.CharField(label='expiration_date', max_length=30)
    state               = forms.CharField(label='state', max_length=20)
    coverage            = forms.CharField(label='coverage', max_length=100)
    year                = forms.CharField(label='year', max_length=4)
    make                = forms.CharField(label='make', max_length=200)
    model               = forms.CharField(label='model', max_length=200)
    vin                 = forms.CharField(label='vin', max_length=30)
    liability_property  = forms.CharField(label='liability_property', max_length=200)
    liability_injury    = forms.CharField(label='liability_injury', max_length=200)
    personal_injury     = forms.CharField(label='personal_injury', max_length=200)
    comprehensive       = forms.CharField(label='comprehensive', max_length=200)
    collision           = forms.CharField(label='collision', max_length=200)
    uninsured_injury    = forms.CharField(label='uninsured_injury', max_length=200)