from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy
from .forms import (InsuredPersonForm, InsuranceTypeForm, InsuranceCoverageForm, PolicyFormFromInsured,
                    PolicyFormFromCoverage, CustomUserCreationForm, UserPolicyForm)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
import logging
from django.db import transaction


# Přiřazení výchozího uživatele k pojištěncům
def assign_default_user_to_insured_persons():
    default_user = User.objects.get(username='default_username')
    InsuredPerson.objects.update(user=default_user)
    return HttpResponse("Assigned default user to all insured persons.")


# Hlavní stránka (index) - zobrazuje seznam pojištěnců
@login_required
def index(request):
    # Admin vidí všechny pojištěnce
    if request.user.is_staff:
        insured_people_list = InsuredPerson.objects.all().order_by('last_name', 'first_name')
    # Běžný uživatel vidí pouze své pojištěnce
    else:
        insured_people_list = InsuredPerson.objects.filter(user=request.user).order_by('last_name', 'first_name')

    paginator = Paginator(insured_people_list, 10)  # počet pojištěnců na stránku

    page_number = request.GET.get('page')
    insured_people = paginator.get_page(page_number)

    return render(request, 'insurance/index.html', {'insured_people': insured_people})


# Detail pojištěnce
@login_required
def insured_detail(request, id):
    # Admin vidí detaily každého pojištěnce
    if request.user.is_staff:
        insured_person = get_object_or_404(InsuredPerson, id=id)
    # Běžný uživatel vidí pouze detaily svého pojištěnce
    else:
        insured_person = get_object_or_404(InsuredPerson, id=id, user=request.user)

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
            messages.error(request, 'Došlo k chybě ve formuláři. Zkontrolujte prosím zadané údaje.')
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
        'insured_person': insured_person  # Předávání pojištěnce do šablony pro případné další zobrazení informací
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


# Odstranění pojištění
def delete_insurance(request, id):
    insurance_type = get_object_or_404(InsuranceType, id=id)

    if request.method == 'POST':
        insurance_type.delete()
        messages.success(request, 'Typ pojištění byl úspěšně odebrán.')
        return redirect('insurance_list')

    return render(
        request, 'insurance/confirm_delete.html', {'object': insurance_type, 'type': 'typ pojištění'}
    )


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

    return render(request, 'insurance/insurance_coverage_form.html',
                  {'form': form, 'insurance_type': insurance_type})


# Odstranění pojistného krytí
def delete_coverage(request, insurance_id, coverage_id):
    coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)

    if request.method == 'POST':
        coverage.delete()
        messages.success(request, 'Pojistné krytí bylo úspěšně odebráno.')
        return redirect('insurance_coverage_list', id=insurance_id)

    return render(
        request, 'insurance/confirm_delete.html', {'object': coverage, 'type': 'pojistné krytí'}
    )


# Přidání pojistky přímo ze stránky pojištěnce
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

    return render(
        request, 'insurance/policy_form.html', {'form': form, 'insured_person': insured_person}
    )


# Přidání pojistky ze stránky pojistného krytí
@login_required
def add_policy_from_coverage(request, coverage_id):
    insurance_coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)
    insured_person = InsuredPerson.objects.filter(user=request.user).first()

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


# Přidání pojistky
@login_required
def create_policy_for_user(request, coverage_id):
    insurance_coverage = get_object_or_404(InsuranceCoverage, id=coverage_id)
    insured_person = InsuredPerson.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserPolicyForm(request.POST, insurance_coverage=insurance_coverage)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.insured_person = insured_person  # Přiřazení aktuálního uživatele jako pojištěné osoby
            policy.insurance_coverage = insurance_coverage
            policy.premium = insurance_coverage.premium
            policy.save()
            messages.success(request, 'Pojištění bylo úspěšně zřízeno.')
            return redirect('insured_detail', id=insured_person.id)
    else:
        form = UserPolicyForm(insurance_coverage=insurance_coverage)

    return render(request, 'insurance/policy_form.html', {
        'form': form,
        'insured_person': insured_person,
        'insurance_coverage': insurance_coverage,
    })


# Editace pojistky
def edit_policy(request, id=None):
    if id:
        policy = get_object_or_404(Policy, id=id)
    else:
        policy = Policy()

    if request.method == 'POST':
        form = PolicyFormFromInsured(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pojištění bylo úspěšně aktualizováno.')
            return redirect('insured_detail', id=policy.insured_person.id)
    else:
        form = PolicyFormFromInsured(instance=policy)
        if not id:
            form.fields['start_date'].initial = (timezone.now() + timezone.timedelta(days=1)).date()

    return render(request, 'insurance/policy_form.html',
                  {'form': form, 'insured_person': policy.insured_person})


# Seznam pojistných krytí
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


# Registrace
logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            id_number = form.cleaned_data.get('id_number')

            # Zalogujeme informace pro ladění
            logger.info(f"Pokouším se vytvořit pojištěnce s e-mailem: {email} a rodným číslem: {id_number}")

            try:
                with transaction.atomic():
                    # Ověření, zda už neexistuje pojištěnec s tímto rodným číslem a emailem
                    if (InsuredPerson.objects.filter(id_number=id_number).exists()
                            or InsuredPerson.objects.filter(email=email).exists()):
                        messages.error(
                            request,
                            "Pojištěnec s tímto e-mailem, rodným číslem nebo telefonním číslem již existuje."
                        )

                        logger.error(
                            f"Pojištěnec s e-mailem {email} nebo rodným číslem {id_number} již existuje."
                        )

                        return render(request, 'insurance/register.html', {'form': form})

                    # Vytvoření uživatele
                    user = form.save()

                    # Vytvoření a přiřazení nového pojištěnce uživateli
                    InsuredPerson.objects.create(
                        user=user,  # Přiřadíme pojištěnce k vytvořenému uživateli
                        first_name=form.cleaned_data.get('first_name'),
                        last_name=form.cleaned_data.get('last_name'),
                        id_number=id_number,
                        email=email,
                        phone_number=form.cleaned_data.get('phone_number'),
                        street_address=form.cleaned_data.get('street_address'),
                        city=form.cleaned_data.get('city'),
                        postal_code=form.cleaned_data.get('postal_code')
                    )

                    # Přihlásíme uživatele po úspěšné registraci
                    login(request, user)
                    messages.success(request, 'Registrace proběhla úspěšně, jste přihlášen(a).')
                    logger.info(f"Pojištěnec s e-mailem {email} a rodným číslem {id_number} byl úspěšně vytvořen.")
                    return redirect('index')

            except Exception as e:
                # Pokud se stane jakákoli chyba, nedojde k uložení uživatele ani pojištěnce
                logger.error(f"Chyba při vytváření pojištěnce: {str(e)}")
                messages.error(request, "Došlo k chybě při registraci. Zkuste to prosím znovu.")
                return render(request, 'insurance/register.html', {'form': form})

    else:
        form = CustomUserCreationForm()

    return render(request, 'insurance/register.html', {'form': form})


# Přihlášení
class CustomLoginView(LoginView):
    def form_valid(self, form):
        messages.success(self.request, f"Jste přihlášen(a) {form.get_user().username}.")
        return super().form_valid(form)


# Odhlášení
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Byl(a) jste úspěšně odhlášen(a).")
        return super().dispatch(request, *args, **kwargs)


def home(request):
    return render(request, 'home.html', {'message': 'Vítejte na naší stránce!'})


# Kontrola, zda je uživatel administrátor
def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def delete_insured(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    if request.method == 'POST':
        insured_person.delete()
        messages.success(request, 'Pojištěnec byl úspěšně odebrán.')
        return redirect('insured_list')
    return render(request, 'insurance/confirm_delete.html', {'object': insured_person})


# Jak na pojištění
def how_to_insurance(request):
    return render(request, 'insurance/how_to_insurance.html')


# O aplikaci
def about(request):
    return render(request, 'insurance/about.html')
