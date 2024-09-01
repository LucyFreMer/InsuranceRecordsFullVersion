from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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


class UserPolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['start_date', 'end_date']  # insured_person bude automaticky nastaveno
        labels = {
            'start_date': 'Datum začátku pojištění',
            'end_date': 'Datum konce pojištění',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        insurance_coverage = kwargs.pop('insurance_coverage', None)
        super(UserPolicyForm, self).__init__(*args, **kwargs)

        # Automatické nastavení prémia na základě pojistného krytí
        if insurance_coverage:
            self.initial['premium'] = insurance_coverage.premium


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label="Uživatelské jméno",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte uživatelské jméno'})
    )
    first_name = forms.CharField(
        required=True,
        label="Jméno",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte křestní jméno'})
    )
    last_name = forms.CharField(
        required=True,
        label="Příjmení",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte příjmení'})
    )
    id_number = forms.CharField(
        required=True,
        label="Rodné číslo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte rodné číslo', 'maxlength': '11'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte email'})
    )
    phone_number = forms.CharField(
        max_length=16,
        required=True,
        label="Telefonní číslo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte telefonní číslo'})
    )
    street_address = forms.CharField(
        required=True,
        label="Ulice a číslo popisné",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte ulici a číslo popisné'})
    )
    city = forms.CharField(
        required=True,
        label="Město",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte město'})
    )
    postal_code = forms.CharField(
        required=True,
        label="PSČ",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte PSČ'})
    )
    password1 = forms.CharField(
        required=True,
        label="Heslo",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte heslo'})
    )
    password2 = forms.CharField(
        required=True,
        label="Potvrzení hesla",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Potvrďte heslo'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'id_number', 'email', 'phone_number', 'street_address', 'city', 'postal_code')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Vytvoření a uložení pojištěnce
            InsuredPerson.objects.create(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                id_number=self.cleaned_data['id_number'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                postal_code=self.cleaned_data['postal_code'],
            )
        return user