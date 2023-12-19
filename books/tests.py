from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from books.models import Book

User = get_user_model()


class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(name='Book1')
        self.book2 = Book.objects.create(name='Book2')
        self.book3 = Book.objects.create(name='Book3')

        self.user = User.objects.create_user(username='user', password='123')

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_book_count(self):
        url = reverse('books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), Book.objects.count())

    def test_book_create(self):
        url = reverse('books')

        response = self.client.post(url, data={'name': 'New book', 'author_name': 'Jon Jones'})

        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertEqual(data['name'], 'New book')

    def test_retrieve_book(self):
        book_id = 3
        url = reverse('book-detail', kwargs={'pk': book_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['id'], book_id)

    def test_update_book(self):
        old_name = self.book3.name
        url = reverse('book-detail', kwargs={'pk': self.book3.id})
        response = self.client.patch(url, data={'name': 'updated name'})

        self.assertEqual(response.status_code, 200)
        self.book3.refresh_from_db()

        # проверить не равен ли старому имени
        self.assertNotEqual(self.book3.name, old_name)

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book3.id})

        self.assertEqual(Book.objects.count(), 3)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        self.assertEqual(Book.objects.count(), 2)
