from django import forms
from .models import InsuredPerson, Policy


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


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['insured_person', 'policy_type', 'coverage_amount', 'premium', 'start_date', 'end_date']
        labels = {
            'insured_person': 'Pojištěná osoba',
            'policy_type': 'Typ pojištění',
            'coverage_amount': 'Výše krytí',
            'premium': 'Pojistné',
            'start_date': 'Datum začátku pojištění',
            'end_date': 'Datum konce pojištění',
        }
