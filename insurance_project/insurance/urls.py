from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('', lambda request: redirect('insured_list'), name='index'),  # Přesměrování na seznam pojištěnců
    path('seznam/', views.index, name='insured_list'),  # Cesta pro seznam pojištěnců
    path('pojistenec/<int:id>/', views.insured_detail, name='insured_detail'),  # Detail konkrétního pojištěnce
    path('pojistenec/pridat/', views.add_insured, name='add_insured'),  # Přidání nového pojištěnce
    path('pojistenec/<int:id>/editovat/', views.edit_insured, name='edit_insured'),  # Editace pojištěnce
    path('pojistenec/<int:id>/odstranit/', views.delete_insured, name='delete_insured'),  # Odstranění pojištěnce

    path('pojisteni/', views.insurance_list, name='insurance_list'),  # Seznam typů pojištění
    path('pojisteni/pridat/', views.add_insurance, name='add_insurance'),  # Přidání nového typu pojištění
    path('pojisteni/editovat/<int:id>/', views.edit_insurance, name='edit_insurance'),  # Editace typu pojištění
    path('pojisteni/odstranit/<int:id>/', views.delete_insurance, name='delete_insurance'),  # Odstranění typu pojištění

    path('pojisteni/<int:id>/kryti/', views.insurance_coverage_list, name='insurance_coverage_list'),  # Zobrazení seznamu pojistných krytí
    path('pojisteni/<int:insurance_id>/kryti/pridat/', views.add_or_edit_coverage, name='add_insurance_coverage'),
    path('pojisteni/<int:insurance_id>/kryti/<int:coverage_id>/editovat/', views.add_or_edit_coverage, name='edit_insurance_coverage'),
    path('pojisteni/<int:insurance_id>/kryti/<int:coverage_id>/odstranit/', views.delete_coverage, name='delete_insurance_coverage'),

    path('pojisteni/<int:id>/', views.policy_detail, name='policy_detail'),  # Detail konkrétního pojištění (pojistky)


    path('pojistenci/<int:insured_id>/zridit_pojistku/', views.add_policy_from_insured, name='add_policy_from_insured'),  # Cesta pro přidání pojištění z detailu pojištěnce
    path('pojisteni/<int:coverage_id>/zridit/', views.add_policy_from_coverage, name='add_policy_from_coverage'),  # Cesta pro přidání pojištění z detailu pojistného krytí


    path('pojistky/<int:id>/editovat/', views.edit_policy, name='edit_policy'),  # Editace pojistky
    path('pojisteni/<int:id>/odstranit/', views.delete_policy, name='delete_policy'),  # Odstranění pojistky

    path('jak-na-pojisteni/', views.how_to_insurance, name='how_to_insurance'),  # Jak na pojištění
    path('o-aplikaci/', views.about, name='about'),  # O aplikaci

    path('registrovat/', views.register, name='register'),  # Registraci
    path('prihlasit/', auth_views.LoginView.as_view(template_name='insurance/login.html'), name='login'),  # Přihlášení
    path('odhlasit/', csrf_exempt(auth_views.LogoutView.as_view(next_page='/')), name='logout'),  # Odhlášení
]