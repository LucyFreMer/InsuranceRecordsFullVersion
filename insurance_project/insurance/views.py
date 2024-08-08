from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import InsuredPerson, Policy
from .forms import InsuredPersonForm, PolicyForm


def index(request):
    return render(request, 'insurance/index.html')


def insured_list(request):
    insured_people = InsuredPerson.objects.all()
    return render(request, 'insurance/insured_list.html', {'insured_people': insured_people})


def insured_detail(request, id):
    insured_person = get_object_or_404(InsuredPerson, id=id)
    return render(request, 'insurance/insured_detail.html', {'insured_person': insured_person})


def add_insured(request):
    if request.method == 'POST':
        form = InsuredPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('insured_list')
    else:
        form = InsuredPersonForm()
    return render(request, 'insurance/add_insured.html', {'form': form})


def policy_detail(request, id):
    policy = get_object_or_404(Policy, id=id)
    return render(request, 'insurance/policy_detail.html', {'policy': policy})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'insurance/register.html', {'form': form})


def login_view(request):
    return render(request, 'insurance/login.html')


def home(request):
    return render(request, 'home.html', {'message': 'Vítejte na naší stránce!'})