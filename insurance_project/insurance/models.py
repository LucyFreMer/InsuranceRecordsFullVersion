from django.db import models


class InsuredPerson(models.Model):
    first_name = models.CharField("Jméno", max_length=100)
    last_name = models.CharField("Příjmení", max_length=100)
    email = models.EmailField("Email")
    phone_number = models.CharField("Telefonní číslo", max_length=16)
    street_address = models.CharField("Ulice a číslo popisné", max_length=255)
    city = models.CharField("Město", max_length=100)
    postal_code = models.CharField("PSČ", max_length=10)


    def __str__(self):
        return f"{self.first_name} {self.last_name}, email: {self.email or 'neuvedeno'}, telefonní číslo: {self.phone_number}, ulice a číslo popisné: {self.street_address or 'neuvedeno'}, město: {self.city}, PSČ: {self.postal_code}"

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