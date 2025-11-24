from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.pets.models import Pet, MedicalRecord, Vaccine
from datetime import date, timedelta


class PetsIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='petowner', password='pw')

    def authenticate_with_jwt(self):
        # obtain JWT token and set Authorization header for subsequent requests
        resp = self.client.post('/api/auth/login/', {'username': 'petowner', 'password': 'pw'}, format='json')
        token = resp.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_pets_empty(self):
        url = '/api/pets/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_pet_requires_auth(self):
        url = '/api/pets/'
        data = {'name': 'Fido', 'species': 'dog', 'age': 3, 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_pet_authenticated(self):
        # authenticate using JWT (the API uses JWTAuthentication)
        self.authenticate_with_jwt()
        url = '/api/pets/'
        data = {'name': 'Fido', 'species': 'dog', 'age': 3, 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pet.objects.filter(name='Fido').exists())


class MedicalRecordIntegrationTests(APITestCase):
    """Tests de integración para el sistema de registros médicos"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='user@test.com')
        self.staff = User.objects.create_user(username='vet', password='testpass123', email='vet@test.com', is_staff=True)
        self.other_user = User.objects.create_user(username='other', password='testpass123', email='other@test.com')
        
        self.pet = Pet.objects.create(name='Firulais', species='Perro', age=3, owner=self.user)
        self.other_pet = Pet.objects.create(name='Michi', species='Gato', age=2, owner=self.other_user)
        
        self.record = MedicalRecord.objects.create(
            pet=self.pet,
            date=date.today(),
            diagnosis='Revisión general',
            treatment='Sin tratamiento',
            veterinarian='Dr. Pérez',
            weight=15.5,
            temperature=38.5
        )
        
        self.vaccine = Vaccine.objects.create(
            pet=self.pet,
            vaccine_name='Rabia',
            date_administered=date.today(),
            next_dose_date=date.today() + timedelta(days=365),
            veterinarian='Dr. Pérez',
            batch_number='LOT123'
        )
    
    def test_list_medical_records_requires_auth(self):
        response = self.client.get('/api/pets/medical-records/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_list_own_pet_records(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/pets/medical-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['pet_name'], 'Firulais')
    
    def test_staff_can_list_all_records(self):
        MedicalRecord.objects.create(
            pet=self.other_pet,
            date=date.today(),
            diagnosis='Chequeo',
            treatment='Vitaminas',
            veterinarian='Dr. López'
        )
        
        self.client.force_authenticate(user=self.staff)
        response = self.client.get('/api/pets/medical-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_staff_can_create_medical_record(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            'pet': self.pet.id,
            'date': str(date.today()),
            'diagnosis': 'Gripe',
            'treatment': 'Antibióticos',
            'veterinarian': 'Dr. García',
            'weight': 16.0,
            'temperature': 39.0,
            'notes': 'Regresar en 1 semana'
        }
        response = self.client.post('/api/pets/medical-records/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalRecord.objects.count(), 2)
    
    def test_user_cannot_create_record_for_others_pet(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'pet': self.other_pet.id,
            'date': str(date.today()),
            'diagnosis': 'Test',
            'treatment': 'Test',
            'veterinarian': 'Dr. Test'
        }
        response = self.client.post('/api/pets/medical-records/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_can_view_own_pet_record_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/pets/medical-records/{self.record.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['diagnosis'], 'Revisión general')
    
    def test_user_cannot_update_medical_record(self):
        self.client.force_authenticate(user=self.user)
        data = {'diagnosis': 'Diagnóstico actualizado'}
        response = self.client.patch(f'/api/pets/medical-records/{self.record.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_can_update_medical_record(self):
        self.client.force_authenticate(user=self.staff)
        data = {'diagnosis': 'Diagnóstico actualizado'}
        response = self.client.patch(f'/api/pets/medical-records/{self.record.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.record.refresh_from_db()
        self.assertEqual(self.record.diagnosis, 'Diagnóstico actualizado')
    
    def test_staff_can_delete_medical_record(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(f'/api/pets/medical-records/{self.record.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalRecord.objects.count(), 0)
    
    def test_user_cannot_delete_medical_record(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/pets/medical-records/{self.record.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_filter_records_by_pet(self):
        pet2 = Pet.objects.create(name='Rex', species='Perro', age=5, owner=self.user)
        MedicalRecord.objects.create(
            pet=pet2,
            date=date.today(),
            diagnosis='Chequeo',
            treatment='OK',
            veterinarian='Dr. Pérez'
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/pets/medical-records/?pet={self.pet.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['pet_name'], 'Firulais')


class VaccineIntegrationTests(APITestCase):
    """Tests de integración para el sistema de vacunas"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.staff = User.objects.create_user(username='vet', password='testpass123', is_staff=True)
        self.pet = Pet.objects.create(name='Firulais', species='Perro', age=3, owner=self.user)
        
        self.vaccine = Vaccine.objects.create(
            pet=self.pet,
            vaccine_name='Rabia',
            date_administered=date.today(),
            next_dose_date=date.today() + timedelta(days=365),
            veterinarian='Dr. Pérez',
            batch_number='LOT123'
        )
    
    def test_list_vaccines_requires_auth(self):
        response = self.client.get('/api/pets/vaccines/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_list_own_pet_vaccines(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/pets/vaccines/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vaccine_name'], 'Rabia')
    
    def test_staff_can_create_vaccine(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            'pet': self.pet.id,
            'vaccine_name': 'Parvovirus',
            'date_administered': str(date.today()),
            'next_dose_date': str(date.today() + timedelta(days=180)),
            'veterinarian': 'Dr. García',
            'batch_number': 'LOT456'
        }
        response = self.client.post('/api/pets/vaccines/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vaccine.objects.count(), 2)
    
    def test_validate_next_dose_date_after_administered(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            'pet': self.pet.id,
            'vaccine_name': 'Test',
            'date_administered': str(date.today()),
            'next_dose_date': str(date.today() - timedelta(days=1)),
            'veterinarian': 'Dr. Test'
        }
        response = self.client.post('/api/pets/vaccines/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('next_dose_date', response.data)
    
    def test_staff_can_update_vaccine(self):
        self.client.force_authenticate(user=self.staff)
        data = {'batch_number': 'LOT999'}
        response = self.client.patch(f'/api/pets/vaccines/{self.vaccine.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vaccine.refresh_from_db()
        self.assertEqual(self.vaccine.batch_number, 'LOT999')
    
    def test_user_cannot_update_vaccine(self):
        self.client.force_authenticate(user=self.user)
        data = {'batch_number': 'LOT999'}
        response = self.client.patch(f'/api/pets/vaccines/{self.vaccine.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_vaccine_is_next_dose_pending_property(self):
        self.assertTrue(self.vaccine.is_next_dose_pending)
        
        vaccine_no_next = Vaccine.objects.create(
            pet=self.pet,
            vaccine_name='Test',
            date_administered=date.today(),
            veterinarian='Dr. Test'
        )
        self.assertFalse(vaccine_no_next.is_next_dose_pending)


class PetMedicalHistoryTests(APITestCase):
    """Tests para el endpoint de historial médico completo"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='user@test.com')
        self.staff = User.objects.create_user(username='vet', password='testpass123', is_staff=True)
        self.other_user = User.objects.create_user(username='other', password='testpass123')
        
        self.pet = Pet.objects.create(name='Firulais', species='Perro', age=3, owner=self.user)
        self.other_pet = Pet.objects.create(name='Michi', species='Gato', age=2, owner=self.other_user)
        
        MedicalRecord.objects.create(
            pet=self.pet,
            date=date.today() - timedelta(days=30),
            diagnosis='Chequeo anual',
            treatment='Vitaminas',
            veterinarian='Dr. Pérez'
        )
        MedicalRecord.objects.create(
            pet=self.pet,
            date=date.today(),
            diagnosis='Revisión',
            treatment='OK',
            veterinarian='Dr. Pérez'
        )
        
        Vaccine.objects.create(
            pet=self.pet,
            vaccine_name='Rabia',
            date_administered=date.today() - timedelta(days=365),
            veterinarian='Dr. Pérez'
        )
        Vaccine.objects.create(
            pet=self.pet,
            vaccine_name='Parvovirus',
            date_administered=date.today(),
            next_dose_date=date.today() + timedelta(days=180),
            veterinarian='Dr. Pérez'
        )
    
    def test_get_pet_medical_history_requires_auth(self):
        response = self.client.get(f'/api/pets/{self.pet.id}/medical-history/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_get_own_pet_medical_history(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/pets/{self.pet.id}/medical-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Firulais')
        self.assertEqual(len(response.data['medical_records']), 2)
        self.assertEqual(len(response.data['vaccines']), 2)
    
    def test_user_cannot_get_other_pet_medical_history(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/pets/{self.other_pet.id}/medical-history/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_staff_can_get_any_pet_medical_history(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f'/api/pets/{self.other_pet.id}/medical-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Michi')
    
    def test_medical_history_includes_owner_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/pets/{self.pet.id}/medical-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner_username'], 'testuser')
        self.assertEqual(response.data['owner_email'], 'user@test.com')
