from django.urls import path
from django.shortcuts import redirect
from .views import CustomLoginView, CustomLogoutView, assign_default_user_to_insured_persons, create_policy_for_user
from . import views


urlpatterns = [
    # Přesměrování na seznam pojištěnců
    path('', lambda request: redirect('insured_list'), name='index'),

    # Seznam pojištěnců
    path('seznam/', views.index, name='insured_list'),

    # Detail konkrétního pojištěnce
    path('pojistenec/<int:id>/', views.insured_detail, name='insured_detail'),

    # Přidání nového pojištěnce
    path('pojistenec/pridat/', views.add_insured, name='add_insured'),

    # Editace pojištěnce
    path('pojistenec/<int:id>/editovat/', views.edit_insured, name='edit_insured'),

    # Odstranění pojištěnce
    path('pojistenec/<int:id>/odstranit/', views.delete_insured, name='delete_insured'),

    # Seznam typů pojištění
    path('pojisteni/', views.insurance_list, name='insurance_list'),

    # Přidání nového typu pojištění
    path('pojisteni/pridat/', views.add_insurance, name='add_insurance'),

    # Editace typu pojištění
    path('pojisteni/editovat/<int:id>/', views.edit_insurance, name='edit_insurance'),

    # Odstranění typu pojištění
    path('pojisteni/odstranit/<int:id>/', views.delete_insurance, name='delete_insurance'),

    # Zobrazení seznamu pojistných krytí
    path('pojisteni/<int:id>/kryti/', views.insurance_coverage_list, name='insurance_coverage_list'),

    # Přidání pojistného krytí
    path('pojisteni/<int:insurance_id>/kryti/pridat/', views.add_or_edit_coverage, name='add_insurance_coverage'),

    # Editace pojistného krytí
    path('pojisteni/<int:insurance_id>/kryti/<int:coverage_id>/editovat/', views.add_or_edit_coverage,
         name='edit_insurance_coverage'),

    # Odstranění pojistného krytí
    path('pojisteni/<int:insurance_id>/kryti/<int:coverage_id>/odstranit/', views.delete_coverage,
         name='delete_insurance_coverage'),

    # Detail konkrétního pojištění (pojistky)
    path('pojisteni/<int:id>/', views.policy_detail, name='policy_detail'),

    # Přidání pojištění z detailu pojištěnce
    path('pojistenci/<int:insured_id>/zridit_pojistku/', views.add_policy_from_insured, name='add_policy_from_insured'),

    # Přidání pojištění z detailu pojistného krytí
    path('pojisteni/<int:coverage_id>/zridit/', views.add_policy_from_coverage, name='add_policy_from_coverage'),

    # Zřízení pojištění uživatelem
    path('pojisteni/<int:coverage_id>/zridit-uzivatelem/', create_policy_for_user, name='create_policy_for_user'),

    # Editace pojistky
    path('pojistky/<int:id>/editovat/', views.edit_policy, name='edit_policy'),

    # Odstranění pojistky
    path('pojisteni/<int:id>/odstranit/', views.delete_policy, name='delete_policy'),

    # Jak na pojištění
    path('jak-na-pojisteni/', views.how_to_insurance, name='how_to_insurance'),

    # O aplikaci
    path('o-aplikaci/', views.about, name='about'),

    # Registrace
    path('registrovat/', views.register, name='register'),

    # Přihlášení
    path('prihlasit/', CustomLoginView.as_view(template_name='insurance/login.html'), name='login'),

    # Odhlášení
    path('odhlasit/', CustomLogoutView.as_view(next_page='login'), name='logout'),

    # Přiřazení výchozího uživatele
    path('assign-default-user/', assign_default_user_to_insured_persons),
]
