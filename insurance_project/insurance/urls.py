from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Domovská stránka
    path('seznam/', views.insured_list, name='insured_list'),  # Seznam pojištěných
    path('<int:id>/', views.insured_detail, name='insured_detail'),  # Detail pojištěného
    path('pridat/', views.add_insured, name='add_insured'),  # Přidání nového pojištěného
    path('pojistka/<int:id>/', views.policy_detail, name='policy_detail'),  # Detail pojištění
    path('registrovat/', views.register, name='register'),
    path('prihlasit/', auth_views.LoginView.as_view(template_name='insurance/login.html'), name='login'),

]