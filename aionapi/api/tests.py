from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from api.models import User, Business, Project, Task

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            str_username='testuser',
            str_email='testuser@example.com',
            str_password='securepassword123',
            fullname='Test User',
            birthday=timezone.now().date() - relativedelta(years=20)
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('securepassword123'))

    def test_user_age_validation(self):
        with self.assertRaises(ValidationError):
            user = User(
                username='younguser',
                email='young@example.com',
                fullname='Young User',
                birthday=timezone.now().date() - relativedelta(years=10) # 10 years old
            )
            user.full_clean() # Triggers validation

    def test_user_fullname_validation(self):
        with self.assertRaises(ValidationError):
            user = User(
                username='badname',
                email='bad@example.com',
                fullname='Bad_Name 123!',
                birthday=timezone.now().date() - relativedelta(years=20)
            )
            user.full_clean()

class BusinessModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            str_username='owner',
            str_email='owner@example.com',
            str_password='password',
            fullname='Business Owner',
            birthday=timezone.now().date() - relativedelta(years=30)
        )

    def test_create_business(self):
        business = Business.objects.create(
            name='Test Business',
            email='contact@testbusiness.com',
            owner=self.user
        )
        self.assertEqual(business.name, 'Test Business')
        self.assertEqual(business.owner, self.user)

class ProjectModelTest(TestCase):
    def test_project_dates_validation(self):
        project = Project(
            name='Invalid Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() - relativedelta(days=5) # End date before start date
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            str_username='owner_t',
            str_email='owner_t@example.com',
            str_password='password',
            fullname='Business Owner',
            birthday=timezone.now().date() - relativedelta(years=30)
        )
        self.project = Project.objects.create(
            name='Valid Project',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + relativedelta(days=5)
        )

    def test_task_dates_validation(self):
        task = Task(
            project=self.project,
            name='Invalid Task',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() - relativedelta(days=5)
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

class UserAuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'apiuser',
            'email': 'apiuser@example.com',
            'password': 'apipassword123',
            'password2': 'apipassword123',
            'fullname': 'Api User',
            'birthday': (timezone.now().date() - relativedelta(years=20)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'apiuser')

    def test_user_login(self):
        # Create user first
        User.objects.create_user(
            str_username='loginuser',
            str_email='login@example.com',
            str_password='loginpass123',
            fullname='Login User',
            birthday=timezone.now().date() - relativedelta(years=20)
        )

        url = reverse('login')
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

