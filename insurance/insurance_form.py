import re
from policy import Policy


# třída pro zpracování vstupů od uživatele
class InsuranceForm:
    def get_first_name(self) -> str:
        # Získání a validace křestního jména, aby nebylo prázdné a neobsahovalo žádná čísla
        while True:
            first_name = input("Zadejte křestní jméno: ").strip()
            if first_name == "":
                print("Křestní jméno nesmí být prázdné.")
            elif any(char.isdigit() for char in first_name):
                print("Křestní jméno nesmí obsahovat číslice.")
            else:
                break
        return first_name

    def get_last_name(self) -> str:
        # Získání a validace příjmení, aby nebylo prázdné a neobsahovalo žádná čísla
        while True:
            last_name = input("Zadejte příjmení: ").strip()
            if last_name == "":
                print("Příjmení nesmí být prázdné.")
            elif any(char.isdigit() for char in last_name):
                print("Příjmení nesmí obsahovat číslice.")
            else:
                break
        return last_name

    def get_age(self) -> int:
        # Získání a validace věku pojištěné osoby
        while True:
            try:
                age = int(input("Zadejte věk: ").strip())
                if age >= 0:
                    break
                print("Věk nesmí být záporné číslo.")
            except ValueError:
                print("Zadali jste neplatný věk. Věk musí být celé číslo.")
        return age

    def get_phone_number(self) -> str:
        # Získání a validace formátu telefonního čísla
        while True:
            phone_number = input('Zadejte telefonní číslo: ').strip()
            if (re.search('^(\\+420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$', phone_number) != None):
                break
            print('Telefonní číslo je ve špatném formátu.')
        return phone_number

    def get_policy_details(self) -> Policy:
        policy_type = input("Zadejte typ pojištění: ").strip()
        coverage_amount = float(input("Zadejte výši krytí: ").strip())
        premium = float(input("Zadejte pojistné: ").strip())
        start_date = input("Zadejte datum začátku pojištění (YYYY-MM-DD): ").strip()
        end_date = input("Zadejte datum konce pojištění (YYYY-MM-DD): ").strip()
        return Policy(policy_type, coverage_amount, premium, start_date, end_date)