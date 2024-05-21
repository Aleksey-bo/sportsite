from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product, Category, City


class TestProductsView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.products_url = reverse('products-list')

        self.category = Category.objects.create(id=1, category_name='Test Category')
        self.user = get_user_model().objects.create_user(id=3, username='testuser', password='testpassword')
        self.location = City.objects.create(id=1, location='Test Location')
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            title='Test Product',
            category=self.category,
            user=self.user,
            description='This is a test product',
            location_product=self.location,
            price=100,
            active=True
        )

    def test_product_creation(self):
        data = {
            'title': 'Test Product',
            'category': self.category.id,
            'user': self.user.id,
            'description': 'This is a test product',
            'location_product': self.location.id,
            'price': 100,
            'active': True,
            'image': []
        }

        response = self.client.post(self.products_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Product.objects.filter(title='Test Product').exists())

    def test_product_deletion(self):
        product_url = reverse('products-detail', args=[self.product.id])
        response = self.client.delete(product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_product_list(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_current_product(self):
        product_url = reverse('products-detail', args=[self.product.id])
        response = self.client.get(product_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
