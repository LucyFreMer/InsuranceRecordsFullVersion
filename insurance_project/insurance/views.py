from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy
from .forms import InsuredPersonForm, InsuranceTypeForm, InsuranceCoverageForm, PolicyFormFromInsured, PolicyFormFromCoverage
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
    policies = Policy.objects.filter(insured_person=insured_person)
    total_premium = sum(policy.premium for policy in policies)

    return render(request, 'insurance/insured_detail.html', {
        'insured_person': insured_person,
        'policies': policies,
        'total_premium': total_premium,
    })


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
            messages.success(request, 'Informace o pojištěnci byly úspěšně aktualizovány.')
            return redirect('insured_detail', id=id)
    else:
        form = InsuredPersonForm(instance=insured_person)

    return render(request, 'insurance/insured_form.html', {
        'form': form,
        'insured_person': insured_person  # Předáváme pojištěnce do šablony pro případné další zobrazení informací
    })


# Odstranění pojištěnce
def delete_insured(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        insured_person.delete()
        messages.success(request, 'Pojištěnec byl úspěšně odebrán.')
        return redirect('insured_list')
    return render(request, 'insurance/confirm_delete.html', {'object': insured_person})


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
            messages.success(request, 'Nový typ pojištění byl úspěšně přidán.')
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
            messages.success(request, 'Typ pojištění byl úspěšně aktualizován.')
            return redirect('insurance_list')
    else:
        form = InsuranceTypeForm(instance=insurance)
    return render(request, 'insurance/insurance_form.html', {'form': form})


def delete_insurance(request, id):
    insurance_type = get_object_or_404(InsuranceType, id=id)

    if request.method == 'POST':
        insurance_type.delete()
        messages.success(request, 'Typ pojištění byl úspěšně odebrán.')
        return redirect('insurance_list')

    return render(request, 'insurance/confirm_delete.html', {'object': insurance_type, 'type': 'typ pojištění'})


# Přidání a úprava pojistného krytí
def add_or_edit_coverage(request, insurance_id, coverage_id=None):
    insurance_type = get_object_or_404(InsuranceType, id=insurance_id)
    if coverage_id:
        coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)
        is_edit = True
    else:
        coverage = InsuranceCoverage(insurance_type=insurance_type)
        is_edit = False

    if request.method == 'POST':
        form = InsuranceCoverageForm(request.POST, instance=coverage)
        if form.is_valid():
            coverage = form.save(commit=False)
            coverage.insurance_type = insurance_type
            coverage.save()
            if is_edit:
                messages.success(request, 'Pojistné krytí bylo úspěšně aktualizováno.')
            else:
                messages.success(request, 'Pojistné krytí bylo úspěšně přidáno.')
            return redirect('insurance_coverage_list', id=insurance_id)
    else:
        form = InsuranceCoverageForm(instance=coverage)

    return render(request, 'insurance/insurance_coverage_form.html', {'form': form, 'insurance_type': insurance_type})


# Odstranění pojistného krytí
def delete_coverage(request, insurance_id, coverage_id):
    coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)

    if request.method == 'POST':
        coverage.delete()
        messages.success(request, 'Pojistné krytí bylo úspěšně odebráno.')
        return redirect('insurance_coverage_list', id=insurance_id)

    return render(request, 'insurance/confirm_delete.html', {'object': coverage, 'type': 'pojistné krytí'})


# Přidání pojistky k pojištěnci
def add_policy_from_insured(request, insured_id):
    insured_person = get_object_or_404(InsuredPerson, id=insured_id)

    if request.method == 'POST':
        form = PolicyFormFromInsured(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.insured_person = insured_person
            policy.premium = policy.insurance_coverage.premium
            policy.save()
            messages.success(request, 'Pojištění bylo úspěšně zřízeno.')
            return redirect('insured_detail', id=insured_id)
    else:
        form = PolicyFormFromInsured()

    return render(request, 'insurance/policy_form.html', {'form': form, 'insured_person': insured_person})


def add_policy_from_coverage(request, coverage_id):
    insurance_coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)

    if request.method == 'POST':
        form = PolicyFormFromCoverage(request.POST, insurance_coverage=insurance_coverage)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.insurance_coverage = insurance_coverage
            policy.premium = insurance_coverage.premium
            policy.save()
            messages.success(request, 'Pojištění bylo úspěšně zřízeno.')
            return redirect('insured_detail', id=policy.insured_person.id)
    else:
        form = PolicyFormFromCoverage(insurance_coverage=insurance_coverage)

    return render(request, 'insurance/policy_form.html', {
        'form': form,
        'insurance_coverage': insurance_coverage
    })


# Editace pojistky
def edit_policy(request, id):
    policy = get_object_or_404(Policy, id=id)

    # Rozhodnutí, který formulář použít
    if policy.insured_person:
        form_class = PolicyFormFromInsured
    else:
        form_class = PolicyFormFromCoverage

    if request.method == 'POST':
        form = form_class(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištění bylo úspěšně aktualizováno.')
            return redirect('insured_detail', id=policy.insured_person.id)
    else:
        # Vytvoření instance formuláře s předvyplněnými údaji
        form = form_class(instance=policy)

    # Pokud formulář používá pojistné krytí, automaticky předvyplníme roční pojistné
    if isinstance(form, PolicyFormFromCoverage):
        initial_premium = policy.insurance_coverage.premium if policy.insurance_coverage else None
    else:
        initial_premium = None

    return render(request, 'insurance/policy_form.html', {
        'form': form,
        'insured_person': policy.insured_person,
        'initial_premium': initial_premium  # Předání počáteční hodnoty ročního pojistného
    })


def insurance_coverage_list(request, id):
    insurance_type = get_object_or_404(InsuranceType, id=id)
    coverage_id = request.GET.get('coverage_id')

    if coverage_id:
        coverages = InsuranceCoverage.objects.filter(insurance_type=insurance_type, id=coverage_id)
    else:
        coverages = InsuranceCoverage.objects.filter(insurance_type=insurance_type)

    return render(request, 'insurance/insurance_coverage_list.html', {
        'insurance_type': insurance_type,
        'coverages': coverages,
    })


# Odstranění pojistky
def delete_policy(request, id):
    policy = get_object_or_404(Policy, id=id)
    insured_id = policy.insured_person.id

    if request.method == 'POST':
        policy.delete()
        messages.success(request, 'Pojištění bylo úspěšně odebráno.')
        return redirect('insured_detail', id=insured_id)

    return render(request, 'insurance/confirm_delete.html', {'object': policy})


# Jak na pojištění
def how_to_insurance(request):
    return render(request, 'insurance/how_to_insurance.html')


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