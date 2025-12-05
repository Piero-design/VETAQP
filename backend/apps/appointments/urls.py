from django.urls import path

from apps.appointments.views import AppointmentListCreateView, AppointmentDetailView

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
]
