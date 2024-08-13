from django.db import models


class InsuredPerson(models.Model):
    first_name = models.CharField("Jméno", max_length=100)
    last_name = models.CharField("Příjmení", max_length=100)
    age = models.IntegerField("Věk")
    phone_number = models.CharField("Telefonní číslo", max_length=16)
    email = models.EmailField("Email", max_length=254, blank=True, null=True)
    address = models.CharField("Adresa", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, věk: {self.age}, telefonní číslo: {self.phone_number}, email: {self.email or 'neuvedeno'}, adresa: {self.address or 'neuvedeno'}"

    class Meta:
        verbose_name = "Pojištěná osoba"
        verbose_name_plural = "Pojištěné osoby"


class Policy(models.Model):
    insured_person = models.ForeignKey(InsuredPerson, related_name='policies', on_delete=models.CASCADE, verbose_name="Pojištěná osoba")
    policy_type = models.CharField("Typ pojištění", max_length=100)
    coverage_amount = models.FloatField("Výše krytí")
    premium = models.FloatField("Pojistné")
    start_date = models.DateField("Datum začátku pojištění")
    end_date = models.DateField("Datum konce pojištění")

    def __str__(self):
        return f"Typ pojištění: {self.policy_type}, Výše krytí: {self.coverage_amount} Kč, Pojistné: {self.premium} Kč, Platnost od: {self.start_date} do: {self.end_date}"

    class Meta:
        verbose_name = "Pojistka"
        verbose_name_plural = "Pojistky"