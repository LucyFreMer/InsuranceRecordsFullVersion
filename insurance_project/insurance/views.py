from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy
from .forms import InsuredPersonForm, InsuranceTypeForm, InsuranceCoverageForm, PolicyForm
from django.core.paginator import Paginator


# Hlavní stránka (index) - zobrazuje seznam pojištěnců
def index(request):
    insured_people_list = InsuredPerson.objects.all()
    paginator = Paginator(insured_people_list, 10)  # počet pojištěnců na stránku

    page_number = request.GET.get('page')
    insured_people = paginator.get_page(page_number)

    return render(request, 'insurance/index.html', {'insured_people': insured_people})


# Detail pojištěnce
def insured_detail(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    return render(request, 'insurance/insured_detail.html', {'insured_person': insured_person})


# Přidání nového pojištěnce
def add_insured(request):
    if request.method == 'POST':
        form = InsuredPersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištěnec byl úspěšně uložen.')
            return redirect('index')
    else:
        form = InsuredPersonForm()
    return render(request, 'insurance/insured_form.html', {'form': form})


# Editace pojištěnce
def edit_insured(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        form = InsuredPersonForm(request.POST, instance=insured_person)
        if form.is_valid():
            form.save()
            return redirect('insured_detail', id=id)
    else:
        form = InsuredPersonForm(instance=insured_person)
    return render(request, 'insurance/insured_form.html', {'form': form})


# Odstranění pojištěnce
def delete_insured(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    insured_person.delete()
    return redirect('index')


# Seznam pojištění
def insurance_list(request):
    insurances = InsuranceType.objects.all()
    return render(request, 'insurance/insurance_list.html', {'insurances': insurances})


# Detail pojištění
def policy_detail(request, id):
    policy = get_object_or_404(Policy, id=id)
    return render(request, 'insurance/policy_detail.html', {'policy': policy})


# Přidání pojištění
def add_insurance(request):
    if request.method == 'POST':
        form = InsuranceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insurance_list')
    else:
        form = InsuranceTypeForm()
    return render(request, 'insurance/insurance_form.html', {'form': form})


# Úprava pojištění
def edit_insurance(request, id):
    insurance = get_object_or_404(InsuranceType, id=id)
    if request.method == 'POST':
        form = InsuranceTypeForm(request.POST, instance=insurance)
        if form.is_valid():
            form.save()
            return redirect('insurance_list')
    else:
        form = InsuranceTypeForm(instance=insurance)
    return render(request, 'insurance/insurance_form.html', {'form': form})


def delete_insurance(request, id):
    insurance_type = get_object_or_404(InsuranceType, id=id)

    if request.method == 'POST':
        insurance_type.delete()
        messages.success(request, 'Typ pojištění byl úspěšně odstraněn.')
        return redirect('insurance_list')

    return render(request, 'insurance/confirm_delete.html', {'object': insurance_type, 'type': 'typ pojištění'})


# Přidání pojistky k pojištěnci
def add_policy(request, insured_id):
    insured_person = get_object_or_404(InsuredPerson, id=insured_id)
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.premium = policy.insurance_coverage.default_premium
            policy.insured_person = insured_person
            policy.save()
            return redirect('insured_detail', id=insured_id)
    else:
        form = PolicyForm()
    return render(request, 'insurance/add_policy.html', {'form': form, 'insured_person': insured_person})


def insurance_coverage_list(request, id):
    insurance_type = get_object_or_404(InsuranceType, id=id)
    coverages = InsuranceCoverage.objects.filter(insurance_type=insurance_type)
    return render(request, 'insurance/insurance_coverage_list.html', {'insurance_type': insurance_type, 'coverages': coverages})


# Editace pojistky
def edit_policy(request, id):
    policy = get_object_or_404(Policy, id=id)
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect('policy_detail', id=id)
    else:
        form = PolicyForm(instance=policy)
    return render(request, 'insurance/add_policy.html', {'form': form})


# Odstranění pojistky
def delete_policy(request, id):
    policy = get_object_or_404(Policy, id=id)
    insured_id = policy.insured_person.id
    policy.delete()
    return redirect('insured_detail', id=insured_id)

# O aplikaci
def about(request):
    return render(request, 'insurance/about.html')


# Registrace
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'insurance/register.html', {'form': form})


def login_view(request):
    return render(request, 'insurance/login.html')


def home(request):
    return render(request, 'home.html', {'message': 'Vítejte na naší stránce!'})