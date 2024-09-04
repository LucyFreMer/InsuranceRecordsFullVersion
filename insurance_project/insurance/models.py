from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class InsuredPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField("Jméno", max_length=50)
    last_name = models.CharField("Příjmení", max_length=30)
    id_number = models.CharField("Rodné číslo", max_length=11)
    email = models.EmailField("Email")
    phone_number = models.CharField("Telefonní číslo", max_length=16)
    street_address = models.CharField("Ulice a číslo popisné", max_length=30)
    city = models.CharField("Město", max_length=30)
    postal_code = models.CharField("PSČ", max_length=6)

    def clean(self):
        """
        Metoda validace pro ověření vstupních dat před uložením do databáze.
        """
        self.validate_id_number()
        self.validate_email()
        self.validate_phone_number()
        self.validate_postal_code()

    def validate_id_number(self):
        """
        Validace rodného čísla – musí mít formát XXXXXX/XXXX a být unikátní.
        """
        if len(self.id_number) != 11 or self.id_number[6] != '/':
            raise ValidationError("Rodné číslo musí být ve formátu 'XXXXXX/XXXX.")
        existing_id_number = InsuredPerson.objects.filter(id_number=self.id_number).exclude(pk=self.pk)
        if existing_id_number.exists():
            raise ValidationError("Toto rodné číslo již bylo použito. Zadejte jiné rodné číslo.")

    def validate_email(self):
        """
        Validace emailu – email musí být unikátní.
        """
        existing_email = InsuredPerson.objects.filter(email=self.email).exclude(pk=self.pk)
        if existing_email.exists():
            raise ValidationError("Tato emailová adresa již byla použita. Zadejte jinou emailovou adresu.")

    def validate_phone_number(self):
        """
        Validace telefonního čísla – musí mít alespoň 9 a maximálně 12 číslic, a být unikátní.
        """
        numeric_value = str(self.phone_number).replace(" ", "").replace("+", "")
        if not numeric_value.isdigit() or len(numeric_value) < 9 or len(numeric_value) > 12:
            raise ValidationError("Telefonní číslo musí mít alespoň 9 a maximálně 12 číslic.")
        existing_phone_number = InsuredPerson.objects.filter(phone_number=self.phone_number).exclude(pk=self.pk)
        if existing_phone_number.exists():
            raise ValidationError("Toto telefonní číslo již bylo použito. Zadejte jiné telefonní číslo.")

    def validate_postal_code(self):
        """
        Validace PSČ – musí obsahovat přesně 5 číslic.
        """
        cleaned_postal_code = str(self.postal_code).replace(" ", "")
        if not cleaned_postal_code.isdigit() or len(cleaned_postal_code) != 5:
            raise ValidationError("PSČ musí obsahovat 5 číslic.")

    def save(self, *args, **kwargs):
        """
        Ukládá model po jeho validaci. Rodné číslo je automaticky upraveno na správný formát.
        """
        self.full_clean()

        if self.id_number and len(str(self.id_number)) == 10:
            self.id_number = str(self.id_number[:6]) + '/' + str(self.id_number[6:])

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
    insurance_type = models.ForeignKey(
        InsuranceType,
        related_name='coverages',
        on_delete=models.CASCADE,
        verbose_name="Typ pojištění"
    )
    name = models.CharField(
        verbose_name="Název pojistného krytí",
        max_length=100
    )
    description = models.TextField(
        verbose_name="Popis pojistného krytí",
        blank=True
    )
    premium = models.FloatField(
        verbose_name="Pojistné",
        default=0.0
    )

    def __str__(self):
        return f"{self.insurance_type.name} - {self.name}"

    class Meta:
        verbose_name = "Pojistné krytí"
        verbose_name_plural = "Pojistná krytí"


class Policy(models.Model):
    insured_person = models.ForeignKey(
        InsuredPerson,
        related_name='policies',
        on_delete=models.CASCADE,
        verbose_name="Pojištěná osoba"
    )
    insurance_coverage = models.ForeignKey(
        InsuranceCoverage,
        on_delete=models.CASCADE,
        verbose_name="Pojistné krytí",
        null=True,
        blank=True
    )
    premium = models.FloatField(
        verbose_name="Pojistné",
        editable=False
    )
    start_date = models.DateField("Datum začátku pojištění")
    end_date = models.DateField("Datum konce pojištění")

    def __str__(self):
        return f"{self.insured_person} - {self.insurance_coverage.name} - Výše pojistného: {self.premium} Kč"

    class Meta:
        verbose_name = "Pojistka"
        verbose_name_plural = "Pojistky"
