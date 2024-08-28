from django import forms
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy
from django.utils.timezone import now
from datetime import timedelta

class InsuredPersonForm(forms.ModelForm):
    class Meta:
        model = InsuredPerson
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'street_address', 'city', 'postal_code']
        labels = {
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'Email',
            'phone_number': 'Telefonní číslo',
            'street_address': 'Ulice a číslo popisné',
            'city': 'Město',
            'postal_code': 'PSČ',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte křestní jméno'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte příjmení'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte telefonní číslo'}),
            'street_address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Zadejte ulici a číslo popisné'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte město'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte PSČ'}),
        }


class InsuranceTypeForm(forms.ModelForm):
    class Meta:
        model = InsuranceType
        fields = ['name', 'description']
        labels = {
            'name': 'Název pojištění',
            'description': 'Popis pojištění',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class InsuranceCoverageForm(forms.ModelForm):
    class Meta:
        model = InsuranceCoverage
        fields = ['insurance_type', 'name', 'description', 'premium']
        labels = {
            'name': 'Název pojistného krytí',
            'description': 'Popis pojistného krytí',
            'premium': 'Roční pojistné',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte název pojistného krytí'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Zadejte popis pojistného krytí'}),
            'premium': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte výši pojistného'}),
        }


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['insured_person', 'insurance_coverage', 'start_date', 'end_date']
        labels = {
            'insured_person': 'Pojištěná osoba',
            'insurance_coverage': 'Pojistné krytí',
            'start_date': 'Datum začátku pojištění',
            'end_date': 'Datum konce pojištění',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),  # Nastavení end_date jako readonly
        }

    def __init__(self, *args, **kwargs):
        super(PolicyForm, self).__init__(*args, **kwargs)
        # Nastavení defaultních hodnot při vytvoření nové pojistky
        if not self.instance.id:
            self.fields['start_date'].initial = now().date() + timedelta(days=1)
            self.fields['end_date'].initial = now().date() + timedelta(days=366)