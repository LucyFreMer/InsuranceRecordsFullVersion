from insured_person import InsuredPerson


# třída pro správu kolekce pojištěných osob
class InsuranceRegistry:
    def __init__(self, insured_people: list[InsuredPerson] = None) -> None:
        if insured_people is None:
            insured_people = []
        self.__insured_people = insured_people

    def add_insured_person(self, person: InsuredPerson) -> None:
        # Přidání pojištěné osoby do seznamu
        self.__insured_people.append(person)

    def list_insured_people(self) -> list[InsuredPerson]:
        # Vrácení seznamu všech pojištěných osob
        return self.__insured_people

    def get_insured_person(self, first_name, last_name) -> list[InsuredPerson]:
        # Vyhledání pojištěné osoby podle jména a příjmení
        return [
            p for p in self.__insured_people
            if p.first_name.lower() == first_name and p.last_name.lower() == last_name
        ]
