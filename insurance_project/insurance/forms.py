from django import forms
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy
from django.utils.timezone import now
from datetime import timedelta


class InsuredPersonForm(forms.ModelForm):
    class Meta:
        model = InsuredPerson
        fields = ['first_name', 'last_name', 'id_number', 'email', 'phone_number', 'street_address', 'city', 'postal_code']
        labels = {
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'id_number': 'Rodné číslo',
            'email': 'Email',
            'phone_number': 'Telefonní číslo',
            'street_address': 'Ulice a číslo popisné',
            'city': 'Město',
            'postal_code': 'PSČ',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte křestní jméno'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte příjmení'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte rodné číslo'}),  # Přidání widgetu pro rodné číslo
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte telefonní číslo'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte ulici a číslo popisné'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte město'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte PSČ'}),
        }

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if len(id_number) == 10:  # Pokud je zadáno rodné číslo bez lomítka
            id_number = id_number[:6] + '/' + id_number[6:]  # Přidání lomítka po 6. číslici
        elif len(id_number) != 11:  # Pokud rodné číslo není ve formátu 6+4 s lomítkem
            raise forms.ValidationError('Rodné číslo musí mít formát "XXXXXX/XXXX".')
        return id_number


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


class PolicyFormFromInsured(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['insurance_coverage', 'start_date', 'end_date']
        labels = {
            'insurance_coverage': 'Pojistné krytí',
            'start_date': 'Datum začátku pojištění',
            'end_date': 'Datum konce pojištění',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(PolicyFormFromInsured, self).__init__(*args, **kwargs)


class PolicyFormFromCoverage(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['insured_person', 'start_date', 'end_date']
        labels = {
            'insured_person': 'Pojištěná osoba',
            'start_date': 'Datum začátku pojištění',
            'end_date': 'Datum konce pojištění',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        # Získání pojistného krytí z argumentů
        insurance_coverage = kwargs.pop('insurance_coverage', None)
        super(PolicyFormFromCoverage, self).__init__(*args, **kwargs)

        # Předání seznamu pojištěnců
        self.fields['insured_person'].queryset = InsuredPerson.objects.all()

        # Automatické nastavení prémia na základě pojistného krytí
        if insurance_coverage:
            self.initial['premium'] = insurance_coverage.premium