from insured_person import InsuredPerson
from insurance_registry import InsuranceRegistry
from insurance_form import InsuranceForm


# hlavní třída řídící běh aplikace a interakci mezi jednotlivými komponentami
class Insurance:
    def __init__(self, registry: InsuranceRegistry, form: InsuranceForm) -> None:
        # Inicializace třídy s registrem pojištěnců a formulářem pro zadávání údajů
        self.__registry = registry
        self.__form = form

    def process_request(self) -> None:
        title = '''
--------------------
Evidence pojištěných
--------------------'''

        choice_description = '''
Vyberte jednu z následujících možností:
1. Přidat nového pojištěného
2. Zobrazit seznam pojištěných
3. Vyhledat pojistného pomocí jména a příjmení
4. Konec

'''
        print(title)
        choice = input(choice_description)
        while choice != "4":
            match choice:
                case "1":
                    # Přidání nového pojištěného
                    self.__registry.add_insured_person(
                        InsuredPerson(
                            self.__form.get_first_name(),
                            self.__form.get_last_name(),
                            self.__form.get_age(),
                            self.__form.get_phone_number()
                        )
                    )
                    print("Pojištěný byl úspěšně přidán.")

                case "2":
                    # Zobrazení seznamu všech pojištěných
                    people = self.__registry.list_insured_people()
                    if people:
                        for person in people:
                            print(person)
                    else:
                        print("Žádné pojištěné osoby nejsou evidovány.")

                case "3":
                    # Vyhledání pojištěného podle jména a příjmení
                    first_name = input("Zadejte křestní jméno: ").strip().lower()
                    last_name = input("Zadejte příjmení: ").strip().lower()
                    people = self.__registry.get_insured_person(first_name, last_name)
                    if people:
                        for person in people:
                            print(person)
                    else:
                        print("Pojištěný nebyl nalezen.")

                case _:
                    print('Neplatná volba, zkuste to znovu.')
            # Načtení dalšího vstupu pro další iteraci
            choice = input(choice_description)
        else:
            print("Ukončuji pojišťovací žádost.")


if __name__ == "__main__":
    Insurance(
        InsuranceRegistry(),
        InsuranceForm()
    ).process_request()
