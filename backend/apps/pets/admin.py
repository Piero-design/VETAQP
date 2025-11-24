from django.contrib import admin
from apps.pets.models import Pet, MedicalRecord, Vaccine


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'age', 'owner']
    list_filter = ['species']
    search_fields = ['name', 'owner__username']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['pet', 'date', 'diagnosis', 'veterinarian', 'created_at']
    list_filter = ['date', 'veterinarian']
    search_fields = ['pet__name', 'diagnosis', 'treatment']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['pet', 'vaccine_name', 'date_administered', 'next_dose_date', 'veterinarian']
    list_filter = ['vaccine_name', 'date_administered']
    search_fields = ['pet__name', 'vaccine_name', 'batch_number']
    date_hierarchy = 'date_administered'
    readonly_fields = ['created_at']
