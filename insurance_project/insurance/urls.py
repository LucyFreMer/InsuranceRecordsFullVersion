from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('', lambda request: redirect('insured_list'), name='index'),  # Přesměrování na seznam pojištěnců
    path('seznam/', views.index, name='insured_list'),  # Cesta pro seznam pojištěnců
    path('pojistenec/<int:id>/', views.insured_detail, name='insured_detail'),  # Detail pojištěnce
    path('pojistenec/pridat/', views.add_insured, name='add_insured'),  # Přidání pojištěnce
    path('pojistenec/<int:id>/editovat/', views.edit_insured, name='edit_insured'),  # Editace pojištěnce
    path('pojistenec/<int:id>/odstranit/', views.delete_insured, name='delete_insured'),  # Odstranění pojištěnce
    path('pojisteni/<int:id>/', views.policy_detail, name='policy_detail'),  # Detail pojištění
    path('pojistenec/<int:insured_id>/pojisteni/pridat/', views.add_policy, name='add_policy'),  # Přidání pojištění
    path('pojisteni/<int:id>/editovat/', views.edit_policy, name='edit_policy'),  # Editace pojištění
    path('pojisteni/<int:id>/odstranit/', views.delete_policy, name='delete_policy'),  # Odstranění pojištění
    path('o-aplikaci/', views.about, name='about'), # O aplikaci
    path('registrovat/', views.register, name='register'),  # Pro registraci
    path('prihlasit/', auth_views.LoginView.as_view(template_name='insurance/login.html'), name='login'),  # Přihlášení
    path('odhlasit/', csrf_exempt(auth_views.LogoutView.as_view(next_page='/')), name='logout'),  # Odhlášení
]