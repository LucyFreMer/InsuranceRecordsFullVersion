from django import forms
from .models import InsuredPerson, Policy


class InsuredPersonForm(forms.ModelForm):
    class Meta:
        model = InsuredPerson
        fields = ['first_name', 'last_name', 'email', 'age', 'phone_number']
        labels = {
            'first_name': 'Křestní jméno',
            'last_name': 'Příjmení',
            'age': 'Věk',
            'phone_number': 'Telefonní číslo'
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
