from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.cache import cache
from datetime import date
from .models import Building, Room, Resident

class BuildingManagementTests(APITestCase):
    def setUp(self):
        """Set up test data and authenticate the client"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test client and force authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.building = Building.objects.create(
            name='Test Building',
            address='123 Test St'
        )
        
        self.room = Room.objects.create(
            number='101',
            building=self.building
        )
        
        self.resident = Resident.objects.create(
            name='John Doe',
            room=self.room,
            date_of_birth=date(1990, 1, 1)
        )
        
        # Clear cache before each test
        cache.clear()
        
        # Define common URLs
        self.list_create_url = reverse('all-data-list-create')
        self.detail_url = lambda pk: reverse('all-data-retrieve-update-destroy', kwargs={'pk': pk})

    def test_list_buildings(self):
        """Test retrieving list of buildings"""
        response = self.client.get(
            f'{self.list_create_url}?type=building',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        self.assertEqual(response.data['results'][0]['name'], 'Test Building')

    def test_create_building(self):
        """Test creating a new building"""
        data = {
            'type': 'building',
            'data': {
                'name': 'New Building',
                'address': '456 New St'
            }
        }
        
        response = self.client.post(
            self.list_create_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(Building.objects.get(name='New Building').address, '456 New St')

    def test_create_room(self):
        """Test creating a new room"""
        data = {
            'type': 'room',
            'data': {
                'number': '102',
                'building': self.building.pk
            }
        }
        
        response = self.client.post(
            self.list_create_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)

    def test_create_resident(self):
        """Test creating a new resident"""
        data = {
            'type': 'resident',
            'data': {
                'name': 'Jane Doe',
                'room': self.room.pk,
                'date_of_birth': '1995-05-15'
            }
        }
        
        response = self.client.post(
            self.list_create_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resident.objects.count(), 2)

    def test_bulk_create_rooms(self):
        """Test bulk creation of rooms"""
        data = {
            'type': 'room',
            'data': [
                {
                    'number': '102',
                    'building': self.building.pk
                },
                {
                    'number': '103',
                    'building': self.building.pk
                }
            ]
        }
        
        response = self.client.post(
            self.list_create_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 3)

    def test_retrieve_building(self):
        """Test retrieving a single building"""
        response = self.client.get(
            f'{self.detail_url(self.building.pk)}?type=building',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Building')

    def test_update_building(self):
        """Test updating a building"""
        data = {
            'type': 'building',
            'data': {
                'name': 'Updated Building',
                'address': '789 Update St'
            }
        }
        
        response = self.client.put(
            self.detail_url(self.building.pk),
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.building.refresh_from_db()
        self.assertEqual(self.building.name, 'Updated Building')

    def test_unique_room_constraint(self):
        """Test that rooms must be unique per building"""
        data = {
            'type': 'room',
            'data': {
                'number': '101',  # Same number as existing room
                'building': self.building.pk
            }
        }
        
        response = self.client.post(
            self.list_create_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_rooms(self):
        """Test retrieving list of rooms"""
        response = self.client.get(
            f'{self.list_create_url}?type=room',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        self.assertEqual(response.data['results'][0]['number'], '101')

    def test_list_residents(self):
        """Test retrieving list of residents"""
        response = self.client.get(
            f'{self.list_create_url}?type=resident',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')

    def test_unauthorized_access(self):
        """Test unauthorized access to endpoints"""
        client = APIClient()
        response = client.get(
            f'{self.list_create_url}?type=building',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_type(self):
        """Test request with invalid entity type"""
        response = self.client.get(
            f'{self.list_create_url}?type=invalid',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_delete_building(self):
        """Test deleting a building and cascade delete"""
        response = self.client.delete(
            f'{self.detail_url(self.building.pk)}?type=building',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Building.objects.count(), 0)
        self.assertEqual(Room.objects.count(), 0)  # Should be deleted due to CASCADE
        self.assertEqual(Resident.objects.count(), 0)  # Should be deleted due to CASCADE

    def tearDown(self):
        """Clean up after each test"""
        cache.clear()
        User.objects.all().delete()
        Building.objects.all().delete()
        Room.objects.all().delete()
        Resident.objects.all().delete()