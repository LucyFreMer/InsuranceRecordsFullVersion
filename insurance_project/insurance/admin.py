from django.contrib import admin
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy


# Model pro pojištěnce
admin.site.register(InsuredPerson)

# Model pro typy pojištění
admin.site.register(InsuranceType)

# Model pro pojistné krytí
admin.site.register(InsuranceCoverage)

# Model pro sjednané pojištění
admin.site.register(Policy)
