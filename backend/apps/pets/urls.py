from django.urls import path
from .views import PetListCreateView, PetDetailView
from apps.pets.views import (
    MedicalRecordListCreateView,
    MedicalRecordDetailView,
    VaccineListCreateView,
    VaccineDetailView,
    PetMedicalHistoryView,
)

urlpatterns = [
    path('', PetListCreateView.as_view(), name='pet_list_create'),
    path('<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('<int:pk>/medical-history/', PetMedicalHistoryView.as_view(), name='pet_medical_history'),
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical_record_list_create'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('vaccines/', VaccineListCreateView.as_view(), name='vaccine_list_create'),
    path('vaccines/<int:pk>/', VaccineDetailView.as_view(), name='vaccine_detail'),
]
