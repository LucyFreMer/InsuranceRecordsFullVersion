from django.db import models


class InsuredPerson(models.Model):
    first_name = models.CharField("Jméno", max_length=100)
    last_name = models.CharField("Příjmení", max_length=100)
    id_number = models.CharField("Rodné číslo", max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField("Email")
    phone_number = models.CharField("Telefonní číslo", max_length=16)
    street_address = models.CharField("Ulice a číslo popisné", max_length=255)
    city = models.CharField("Město", max_length=100)
    postal_code = models.CharField("PSČ", max_length=10)

    def save(self, *args, **kwargs):
        if self.id_number and len(self.id_number) == 10:
            self.id_number = self.id_number[:6] + '/' + self.id_number[6:]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Pojištěná osoba"
        verbose_name_plural = "Pojištěné osoby"


class InsuranceType(models.Model):
    name = models.CharField("Název typu pojištění", max_length=100)
    description = models.TextField("Popis typu pojištění", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Typ pojištění"
        verbose_name_plural = "Typy pojištění"


class InsuranceCoverage(models.Model):
    insurance_type = models.ForeignKey(InsuranceType, related_name='coverages', on_delete=models.CASCADE, verbose_name="Typ pojištění")
    name = models.CharField("Název pojistného krytí", max_length=100)
    description = models.TextField("Popis pojistného krytí", blank=True)
    premium = models.FloatField("Pojistné", default=0.0)

    def __str__(self):
        return f"{self.insurance_type.name} - {self.name}"

    class Meta:
        verbose_name = "Pojistné krytí"
        verbose_name_plural = "Pojistná krytí"


class Policy(models.Model):
    insured_person = models.ForeignKey(InsuredPerson, related_name='policies', on_delete=models.CASCADE, verbose_name="Pojištěná osoba")
    insurance_coverage = models.ForeignKey(InsuranceCoverage, on_delete=models.CASCADE, verbose_name="Pojistné krytí", null=True, blank=True)
    premium = models.FloatField("Pojistné", editable=False)
    start_date = models.DateField("Datum začátku pojištění")
    end_date = models.DateField("Datum konce pojištění")

    def __str__(self):
        return f"{self.insurance_coverage.name} - Výše pojistného: {self.premium} Kč"

    class Meta:
        verbose_name = "Pojistka"
        verbose_name_plural = "Pojistky"