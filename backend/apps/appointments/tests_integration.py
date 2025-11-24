from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, time
from apps.appointments.models import Appointment
from apps.pets.models import Pet


class AppointmentIntegrationTests(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Crear mascota de prueba
        self.pet = Pet.objects.create(
            owner=self.user,
            name='Max',
            species='dog',
            age=3
        )
        
        # Fecha y hora futuras
        self.future_date = timezone.now().date() + timedelta(days=7)
        self.appointment_time = time(10, 0)  # 10:00 AM
    
    def test_list_appointments_requires_auth(self):
        """Listar citas requiere autenticación"""
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_appointment(self):
        """Crear una cita"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'pet': self.pet.id,
            'appointment_date': self.future_date.isoformat(),
            'appointment_time': '10:00:00',
            'reason': 'Consulta general',
            'veterinarian': 'Dr. García',
            'notes': 'Primera consulta'
        }
        
        response = self.client.post('/api/appointments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'SCHEDULED')
        self.assertEqual(response.data['reason'], 'Consulta general')
    
    def test_create_appointment_past_date(self):
        """No permite crear cita en fecha pasada"""
        self.client.force_authenticate(user=self.user)
        
        past_date = timezone.now().date() - timedelta(days=1)
        data = {
            'pet': self.pet.id,
            'appointment_date': past_date.isoformat(),
            'appointment_time': '10:00:00',
            'reason': 'Consulta'
        }
        
        response = self.client.post('/api/appointments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('appointment_date', response.data)
    
    def test_create_appointment_invalid_time(self):
        """No permite crear cita fuera del horario de atención"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'pet': self.pet.id,
            'appointment_date': self.future_date.isoformat(),
            'appointment_time': '22:00:00',  # 10 PM - fuera de horario
            'reason': 'Consulta'
        }
        
        response = self.client.post('/api/appointments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('appointment_time', response.data)
    
    def test_list_appointments(self):
        """Listar citas del usuario autenticado"""
        self.client.force_authenticate(user=self.user)
        
        # Crear cita
        appointment = Appointment.objects.create(
            user=self.user,
            pet=self.pet,
            appointment_date=self.future_date,
            appointment_time=self.appointment_time,
            reason='Vacunación'
        )
        
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], appointment.id)
        self.assertEqual(response.data[0]['pet_name'], 'Max')
    
    def test_appointment_detail(self):
        """Ver detalle de una cita"""
        self.client.force_authenticate(user=self.user)
        
        appointment = Appointment.objects.create(
            user=self.user,
            pet=self.pet,
            appointment_date=self.future_date,
            appointment_time=self.appointment_time,
            reason='Chequeo'
        )
        
        response = self.client.get(f'/api/appointments/{appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], appointment.id)
        self.assertEqual(response.data['reason'], 'Chequeo')
    
    def test_filter_appointments_by_status(self):
        """Filtrar citas por estado"""
        self.client.force_authenticate(user=self.user)
        
        # Crear citas con diferentes estados
        Appointment.objects.create(
            user=self.user, pet=self.pet,
            appointment_date=self.future_date,
            appointment_time=self.appointment_time,
            reason='Consulta 1', status='SCHEDULED'
        )
        Appointment.objects.create(
            user=self.user, pet=self.pet,
            appointment_date=self.future_date + timedelta(days=1),
            appointment_time=self.appointment_time,
            reason='Consulta 2', status='CONFIRMED'
        )
        
        # Filtrar por SCHEDULED
        response = self.client.get('/api/appointments/?status=SCHEDULED')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'SCHEDULED')
    
    def test_cancel_appointment(self):
        """Cancelar una cita (DELETE)"""
        self.client.force_authenticate(user=self.user)
        
        appointment = Appointment.objects.create(
            user=self.user,
            pet=self.pet,
            appointment_date=self.future_date,
            appointment_time=self.appointment_time,
            reason='Consulta'
        )
        
        response = self.client.delete(f'/api/appointments/{appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se canceló (no se eliminó)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, 'CANCELLED')
