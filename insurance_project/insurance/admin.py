from django.contrib import admin
from .models import InsuredPerson, InsuranceType, InsuranceCoverage, Policy

admin.site.register(InsuredPerson)
admin.site.register(InsuranceType)
admin.site.register(InsuranceCoverage)
admin.site.register(Policy)


