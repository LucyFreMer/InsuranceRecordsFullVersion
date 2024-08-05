# třída pro reprezentaci pojištěné osoby
class InsuredPerson:
    def __init__(self, first_name: str, last_name: str, age: int, phone_number: str) -> None:
        # Inicializace atributů pojištěné osoby
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone_number = phone_number
        self.policies = []

    def add_policy(self, policy):
        self.policies.append(policy)

    def __str__(self):
        policies_str = "\n".join([str(policy) for policy in self.policies])
        # Vrácení textové reprezentace pojištěné osoby
        return f"{self.first_name} {self.last_name}, věk: {self.age}, telefonní číslo: {self.phone_number}\nPojištění:\n{policies_str}"
